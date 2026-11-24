[assembly: UnityEngine.Scripting.AlwaysLinkAssembly]

namespace Project.Persistence
{
    using System;
    using System.IO;
    using System.Threading;
    using System.Threading.Tasks;
    using Project.Core;
    using SQLite;
    using UnityEngine;

    /// <summary>Initializes SQLite and implements the typed game database interface.</summary>
    public sealed partial class GameDatabase : IGameDatabase
    {
        private const int SupportedSchemaVersion = 1;
        private const string SchemaVersionPragma = "PRAGMA user_version;";
        private const string ForeignKeysPragma = "PRAGMA foreign_keys = ON;";
        private const string DatabaseFileName = "tohannic.db";
        private const string SchemaResource = "Tohannic/Database/schema.sql";
        private const string SeedResource = "Tohannic/Database/seed.sql";

        private readonly string _databasePath;

        /// <summary>Initializes a new instance of the <see cref="GameDatabase"/> class.</summary>
        /// <param name="databasePath">The path of an initialized database.</param>
        private GameDatabase(string databasePath)
        {
            this._databasePath = databasePath;
        }

        /// <summary>Opens the game's database in Unity's persistent data directory.</summary>
        /// <returns>The game database or a database error.</returns>
        public static Task<Result<IGameDatabase, DatabaseError>> OpenAsync()
        {
            return OpenAsync(
                Path.Combine(Application.persistentDataPath, DatabaseFileName)
            );
        }

        /// <summary>Opens a database file and initializes its catalog on first use.</summary>
        /// <param name="databasePath">The path of the writable SQLite file.</param>
        /// <returns>The game database or a database error.</returns>
        public static Task<Result<IGameDatabase, DatabaseError>> OpenAsync(
            string databasePath
        )
        {
            if (string.IsNullOrWhiteSpace(databasePath))
            {
                return FailedAsync<IGameDatabase>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.DatabasePathRequired
                );
            }

            // Unity text assets are read on the calling thread before starting the SQLite job.
            string schema = LoadSql(SchemaResource);
            string seed = LoadSql(SeedResource);
            return RunAsync(() => OpenDatabase(databasePath, schema, seed));
        }

        /// <summary>Prepares the default database when gameplay starts.</summary>
        [RuntimeInitializeOnLoadMethod(
            RuntimeInitializeLoadType.BeforeSceneLoad
        )]
        private static void InitializeLocalDatabase()
        {
            _ = ReportInitializationAsync();
        }

        /// <summary>Reports a failed startup initialization in the Unity log.</summary>
        /// <returns>The task that observes the initialization.</returns>
        private static async Task ReportInitializationAsync()
        {
            Result<IGameDatabase, DatabaseError> result = await OpenAsync();
            if (result.TryGetError(out DatabaseError error))
            {
                string message = error.Message;
                if (!string.IsNullOrEmpty(error.TechnicalDetails))
                {
                    message += Environment.NewLine + error.TechnicalDetails;
                }

                Debug.LogError(message);
            }
        }

        /// <summary>Initializes the schema and initial data together when the database is new.</summary>
        /// <param name="databasePath">The path of the writable SQLite file.</param>
        /// <param name="schema">The packaged database schema.</param>
        /// <param name="seed">The packaged initial catalog.</param>
        /// <returns>The initialized database or a storage error.</returns>
        private static Result<IGameDatabase, DatabaseError> OpenDatabase(
            string databasePath,
            string schema,
            string seed
        )
        {
            string fullPath = Path.GetFullPath(databasePath);
            Directory.CreateDirectory(Path.GetDirectoryName(fullPath));

            using SQLiteConnection connection = new SQLiteConnection(fullPath);
            connection.Execute(ForeignKeysPragma);
            int version = connection.ExecuteScalar<int>(SchemaVersionPragma);
            if (version != 0)
            {
                return ExistingDatabase(fullPath, version);
            }

            // Recheck under the write lock in case another connection initialized the file.
            connection.Execute("BEGIN IMMEDIATE;");
            version = connection.ExecuteScalar<int>(SchemaVersionPragma);
            if (version != 0)
            {
                connection.Execute("COMMIT;");
                return ExistingDatabase(fullPath, version);
            }

            if (schema == null || seed == null)
            {
                return Failure<IGameDatabase>(
                    DatabaseErrorCode.MissingResource,
                    DatabaseErrorMessages.SchemaResourcesMissing
                );
            }

            connection.ExecuteScript(schema);
            connection.ExecuteScript(seed);
            connection.Execute("COMMIT;");
            return Result<IGameDatabase, DatabaseError>.Ok(
                new GameDatabase(fullPath)
            );
        }

        /// <summary>Admits a database with the supported schema version.</summary>
        /// <param name="path">The path of the database file.</param>
        /// <param name="version">The schema version read from SQLite.</param>
        /// <returns>The existing database or a schema version error.</returns>
        private static Result<IGameDatabase, DatabaseError> ExistingDatabase(
            string path,
            int version
        )
        {
            if (version != SupportedSchemaVersion)
            {
                return Failure<IGameDatabase>(
                    DatabaseErrorCode.UnsupportedSchema,
                    DatabaseErrorMessages.UnsupportedSchema(version)
                );
            }

            return Result<IGameDatabase, DatabaseError>.Ok(
                new GameDatabase(path)
            );
        }

        /// <summary>Reads a SQL script packaged as a Unity text asset.</summary>
        /// <param name="resourcePath">The path relative to a Resources folder.</param>
        /// <returns>The script text, if present.</returns>
        private static string LoadSql(string resourcePath)
        {
            TextAsset asset = Resources.Load<TextAsset>(resourcePath);
            return asset == null ? null : asset.text;
        }

        /// <summary>Runs SQLite work off the Unity thread and observes its completion.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="operation">The database work to schedule.</param>
        /// <returns>A task producing a typed result.</returns>
        private static Task<Result<T, DatabaseError>> RunAsync<T>(
            Func<Result<T, DatabaseError>> operation
        )
        {
            return Task.Run(operation)
                .ContinueWith(
                    CompleteOperation<T>,
                    CancellationToken.None,
                    TaskContinuationOptions.ExecuteSynchronously,
                    TaskScheduler.Default
                )
                .Unwrap();
        }

        /// <summary>Converts a failed SQLite-net task into the project's result type.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="operation">The completed database task.</param>
        /// <returns>The database result.</returns>
        private static Task<Result<T, DatabaseError>> CompleteOperation<T>(
            Task<Result<T, DatabaseError>> operation
        )
        {
            if (operation.IsCompletedSuccessfully)
            {
                return operation;
            }

            Exception exception = operation.Exception?.GetBaseException();
            DatabaseErrorCode code = DatabaseErrorCode.Storage;
            if (exception is SQLiteException sqlite)
            {
                code = sqlite.Result switch
                {
                    SQLite3.Result.Constraint => DatabaseErrorCode.Constraint,
                    SQLite3.Result.Busy or SQLite3.Result.Locked =>
                        DatabaseErrorCode.Busy,
                    _ => DatabaseErrorCode.Storage,
                };
            }
            else if (exception is ArgumentException)
            {
                code = DatabaseErrorCode.InvalidInput;
            }

            return Task.FromResult(
                Result<T, DatabaseError>.Fail(
                    new DatabaseError(
                        code,
                        DatabaseErrorMessages.ForOperationFailure(code),
                        exception?.Message
                    )
                )
            );
        }

        /// <summary>Produces a failed database result.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="code">The kind of database failure.</param>
        /// <param name="message">The reason for the failure.</param>
        /// <returns>The failed result.</returns>
        private static Result<T, DatabaseError> Failure<T>(
            DatabaseErrorCode code,
            string message
        )
        {
            return Result<T, DatabaseError>.Fail(
                new DatabaseError(code, message)
            );
        }

        /// <summary>Produces an already completed task containing a database error.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="code">The kind of database failure.</param>
        /// <param name="message">The reason for the failure.</param>
        /// <returns>The completed failed result.</returns>
        private static Task<Result<T, DatabaseError>> FailedAsync<T>(
            DatabaseErrorCode code,
            string message
        )
        {
            return Task.FromResult(Failure<T>(code, message));
        }

        /// <summary>Runs a typed operation on a connection owned by the worker.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="operation">The operation using the open SQLite connection.</param>
        /// <returns>The asynchronous result of the operation.</returns>
        private Task<Result<T, DatabaseError>> WithConnectionAsync<T>(
            Func<SQLiteConnection, Result<T, DatabaseError>> operation
        )
        {
            return RunAsync(() =>
            {
                using SQLiteConnection connection = new SQLiteConnection(
                    this._databasePath,
                    SQLiteOpenFlags.ReadWrite
                );
                connection.Execute(ForeignKeysPragma);
                return operation(connection);
            });
        }

        /// <summary>Runs an ORM query and returns its value on success.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="query">The query using the open SQLite connection.</param>
        /// <returns>The asynchronous result of the query.</returns>
        private Task<Result<T, DatabaseError>> QueryAsync<T>(
            Func<SQLiteConnection, T> query
        )
        {
            return this.WithConnectionAsync(connection =>
                Result<T, DatabaseError>.Ok(query(connection))
            );
        }
    }
}
