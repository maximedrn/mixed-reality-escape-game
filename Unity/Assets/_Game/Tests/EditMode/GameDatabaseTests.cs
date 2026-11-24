namespace Project.Tests.EditMode
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Threading.Tasks;
    using NUnit.Framework;
    using Project.Core;
    using Project.Persistence;
    using SQLite;

    /// <summary>Exercises the database integration with the packaged schema and SQLite library.</summary>
    public sealed class GameDatabaseTests
    {
        private const string SchemaVersionPragma = "PRAGMA user_version;";

        private string _databasePath;

        /// <summary>Allocates a separate database path for each test.</summary>
        [SetUp]
        public void SetUp()
        {
            this._databasePath = Path.Combine(
                Path.GetTempPath(),
                $"tohannic-{Guid.NewGuid():N}.db"
            );
        }

        /// <summary>Removes the temporary database after its connections close.</summary>
        [TearDown]
        public void TearDown()
        {
            File.Delete(this._databasePath);
        }

        /// <summary>The first open installs the schema and initial difficulty catalog.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task FirstOpenInstallsCatalog()
        {
            Unwrap(await GameDatabase.OpenAsync(this._databasePath));
            using SQLiteConnection reader = new SQLiteConnection(
                this._databasePath,
                SQLiteOpenFlags.ReadOnly
            );

            Assert.That(
                reader.ExecuteScalar<int>(SchemaVersionPragma),
                Is.EqualTo(1)
            );
            Assert.That(
                reader.ExecuteScalar<int>("SELECT count(*) FROM difficulties;"),
                Is.EqualTo(5)
            );
        }

        /// <summary>Reopening preserves players and skips the initial inserts.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task ReopenPreservesPlayers()
        {
            IGameDatabase database = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            string playerId = Unwrap(await database.AddPlayerAsync("Ada")).Id;
            Unwrap(await database.RenamePlayerAsync(playerId, "Élie"));
            IGameDatabase reopened = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            IReadOnlyList<PlayerRow> players = Unwrap(
                await reopened.ReadPlayersAsync()
            );
            Assert.That(players, Has.Count.EqualTo(1));
            Assert.That(players[0].Id, Is.EqualTo(playerId));
            Assert.That(players[0].DisplayName, Is.EqualTo("Élie"));
            Assert.That(
                Unwrap(await reopened.ReadPlayerAsync(playerId)).DisplayName,
                Is.EqualTo("Élie")
            );
        }

        /// <summary>The leaderboard view returns a typed, version-scoped result.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task ReadLeaderboardMapsRankedSession()
        {
            const int DurationMs = 1250;
            IGameDatabase database = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            PlayerRow player = Unwrap(await database.AddPlayerAsync("Élie"));
            using (
                SQLiteConnection writer = new SQLiteConnection(
                    this._databasePath
                )
            )
            {
                InsertLeaderboardFixture(writer);
                writer.Execute(
                    @"INSERT INTO game_sessions (
                        id, player_id, content_version_id, ruleset_id, room_id,
                        started_at_utc_ms, finished_at_utc_ms, duration_ms, outcome, leaderboard_eligible
                    ) VALUES ('win', ?, 'documentation-001', 'normal', 'room', 0, ?, ?, 'Won', 1);",
                    player.Id,
                    DurationMs,
                    DurationMs
                );
            }

            IReadOnlyList<LeaderboardEntryRow> entries = Unwrap(
                await database.ReadLeaderboardAsync(
                    "documentation-001",
                    "normal",
                    1
                )
            );
            Assert.That(entries, Has.Count.EqualTo(1));
            Assert.That(entries[0].Rank, Is.EqualTo(1));
            Assert.That(entries[0].PlayerId, Is.EqualTo(player.Id));
            Assert.That(entries[0].DisplayName, Is.EqualTo("Élie"));
            Assert.That(entries[0].DurationMs, Is.EqualTo(DurationMs));
            Assert.That(
                Unwrap(
                    await database.ReadLeaderboardAsync(
                        "other-version",
                        "normal",
                        1
                    )
                ),
                Is.Empty
            );
        }

        /// <summary>A failed first initialization rolls back its earlier schema statements.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task FailedInitializationRollsBack()
        {
            using (
                SQLiteConnection writer = new SQLiteConnection(
                    this._databasePath
                )
            )
            {
                writer.Execute("CREATE TABLE items (id TEXT PRIMARY KEY);");
            }

            Result<IGameDatabase, DatabaseError> result =
                await GameDatabase.OpenAsync(this._databasePath);
            Assert.That(result.TryGetError(out DatabaseError error), Is.True);
            Assert.That(error.Code, Is.EqualTo(DatabaseErrorCode.Storage));
            Assert.That(
                error.Message,
                Is.EqualTo("The database operation did not complete.")
            );
            Assert.That(error.TechnicalDetails, Does.Contain("items"));
            using SQLiteConnection reader = new SQLiteConnection(
                this._databasePath,
                SQLiteOpenFlags.ReadOnly
            );
            Assert.That(
                reader.ExecuteScalar<int>(
                    "SELECT count(*) FROM sqlite_schema WHERE type = 'table';"
                ),
                Is.EqualTo(1)
            );
            Assert.That(
                reader.ExecuteScalar<int>(SchemaVersionPragma),
                Is.Zero
            );
        }

        /// <summary>An existing database with an unknown version is rejected without modification.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task UnknownSchemaVersionIsPreserved()
        {
            using (
                SQLiteConnection writer = new SQLiteConnection(
                    this._databasePath
                )
            )
            {
                writer.Execute("PRAGMA user_version = 2;");
            }

            Result<IGameDatabase, DatabaseError> result =
                await GameDatabase.OpenAsync(this._databasePath);
            Assert.That(result.TryGetError(out DatabaseError error), Is.True);
            Assert.That(
                error.Code,
                Is.EqualTo(DatabaseErrorCode.UnsupportedSchema)
            );
            Assert.That(
                error.Message,
                Is.EqualTo("Unsupported Tohannic database schema version 2.")
            );
            using SQLiteConnection reader = new SQLiteConnection(
                this._databasePath,
                SQLiteOpenFlags.ReadOnly
            );
            Assert.That(
                reader.ExecuteScalar<int>(SchemaVersionPragma),
                Is.EqualTo(2)
            );
        }

        /// <summary>An empty name returns a validation result through the game database interface.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task InvalidPlayerNameReturnsFailure()
        {
            IGameDatabase database = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            AssertFailure(
                await database.AddPlayerAsync(" "),
                DatabaseErrorCode.InvalidInput
            );
            Assert.That(Unwrap(await database.ReadPlayersAsync()), Is.Empty);
        }

        /// <summary>The seeded catalog is available by version while activation is explicit.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task ReadCatalogReturnsVersionedConfiguration()
        {
            const int DifficultyCount = 5;
            IGameDatabase database = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            GameCatalog catalog = Unwrap(
                await database.ReadCatalogAsync("documentation-001")
            );

            Assert.That(
                catalog.Difficulties,
                Has.Count.EqualTo(DifficultyCount)
            );
            Assert.That(catalog.Difficulties[0].Id, Is.EqualTo("Peaceful"));
            Assert.That(
                catalog.Items,
                Has.Some.Property(nameof(ItemRow.Id)).EqualTo("chain")
            );
            AssertFailure(
                await database.ReadActiveCatalogAsync(),
                DatabaseErrorCode.NotFound
            );
        }

        /// <summary>A finished session can be recorded and read from the player's history.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task SaveFinishedSessionReturnsTypedStatistics()
        {
            IGameDatabase database = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            PlayerRow player = Unwrap(await database.AddPlayerAsync("Ada"));
            using (
                SQLiteConnection writer = new SQLiteConnection(
                    this._databasePath
                )
            )
            {
                InsertLeaderboardFixture(writer);
            }

            GameSessionRecord record = CreateFinishedSession(player.Id);

            Unwrap(await database.SaveSessionAsync(record));
            GameSessionRecord stored = Unwrap(
                await database.ReadSessionAsync(record.Session.Id)
            );

            Assert.That(stored.RoomCalibration.FixedMarkersSeen, Is.EqualTo(1));
            Assert.That(
                Unwrap(await database.ReadSessionsAsync(player.Id)),
                Has.Count.EqualTo(1)
            );
            Assert.That(
                Unwrap(await database.ReadPlayerStatsAsync(player.Id))[0].Wins,
                Is.EqualTo(1)
            );
        }

        /// <summary>A rejected measurement rolls back the entire session write.</summary>
        /// <returns>The asynchronous test.</returns>
        [Test]
        public async Task InvalidCalibrationRollsBackTheSession()
        {
            IGameDatabase database = Unwrap(
                await GameDatabase.OpenAsync(this._databasePath)
            );
            PlayerRow player = Unwrap(await database.AddPlayerAsync("Ada"));
            using (
                SQLiteConnection writer = new SQLiteConnection(
                    this._databasePath
                )
            )
            {
                InsertLeaderboardFixture(writer);
            }

            GameSessionRecord record = CreateFinishedSession(player.Id);
            record.RoomCalibration.DurationMs = -1;

            AssertFailure(
                await database.SaveSessionAsync(record),
                DatabaseErrorCode.Constraint
            );
            AssertFailure(
                await database.ReadSessionAsync(record.Session.Id),
                DatabaseErrorCode.NotFound
            );
            Assert.That(
                Unwrap(await database.ReadSessionsAsync(player.Id)),
                Is.Empty
            );
        }

        /// <summary>Builds a finished session for the test ruleset.</summary>
        /// <param name="playerId">The local player associated with the result.</param>
        /// <returns>The completed session and its room calibration.</returns>
        private static GameSessionRecord CreateFinishedSession(string playerId)
        {
            return new GameSessionRecord
            {
                Session = new GameSessionRow
                {
                    Id = "session",
                    PlayerId = playerId,
                    ContentVersionId = "documentation-001",
                    RulesetId = "normal",
                    RoomId = "room",
                    StartedAtUtcMs = 0,
                    FinishedAtUtcMs = 1,
                    DurationMs = 1,
                    Outcome = "Won",
                    LeaderboardEligible = 1,
                },
                RoomCalibration = new SessionRoomCalibrationRow
                {
                    SessionId = "session",
                    FixedMarkersSeen = 1,
                },
            };
        }

        /// <summary>Extracts a successful database result for subsequent assertions.</summary>
        /// <typeparam name="T">The expected returned value type.</typeparam>
        /// <param name="result">The database result.</param>
        /// <returns>The successfully returned value.</returns>
        private static T Unwrap<T>(Result<T, DatabaseError> result)
        {
            bool succeeded = result.TryGetValue(out T value);
            result.TryGetError(out DatabaseError error);
            Assert.That(succeeded, Is.True, error.Message);
            return value;
        }

        /// <summary>Checks that a database result contains the expected error code.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="result">The database result.</param>
        /// <param name="code">The expected database error code.</param>
        private static void AssertFailure<T>(
            Result<T, DatabaseError> result,
            DatabaseErrorCode code
        )
        {
            Assert.That(result.TryGetError(out DatabaseError error), Is.True);
            Assert.That(error.Code, Is.EqualTo(code));
        }

        /// <summary>Publishes a minimal ruleset with a leaderboard in the test database.</summary>
        /// <param name="writer">The open connection used to insert the fixture.</param>
        private static void InsertLeaderboardFixture(SQLiteConnection writer)
        {
            writer.ExecuteScript(
                @"PRAGMA foreign_keys = ON;
                INSERT INTO published_content_versions VALUES ('documentation-001', 0);
                INSERT INTO asset_refs VALUES ('documentation-001', 'scene', 'test/scene', 'Scene');
                INSERT INTO rooms (content_version_id, id, label, scene_asset_id)
                    VALUES ('documentation-001', 'room', 'Test room', 'scene');
                INSERT INTO room_anchors VALUES ('documentation-001', 'room', 'origin', 0, 0, 0, 0, 0, 0, 1);
                INSERT INTO interaction_profiles VALUES
                    ('documentation-001', 'hands', 0.1, 0.1, 0.1, 1, 1, 1, 1, 0, 1000, 5, 0);
                INSERT INTO physics_profiles VALUES ('documentation-001', 'physics', 0, 1);
                INSERT INTO scenarios VALUES
                    ('documentation-001', 'scenario', 'room', 'Test scenario', 'origin', 'origin', 'hands', 'physics');
                INSERT INTO rulesets VALUES ('documentation-001', 'normal', 'scenario', 'room', 'Normal');
                INSERT INTO leaderboards VALUES ('documentation-001', 'normal', 'room', NULL, 10);"
            );
        }
    }
}
