namespace Project.Persistence
{
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading.Tasks;
    using Project.Core;
    using SQLite;

    public sealed partial class GameDatabase
    {
        /// <inheritdoc/>
        public Task<
            Result<IReadOnlyList<GameSessionRow>, DatabaseError>
        > ReadSessionsAsync(string playerId)
        {
            if (string.IsNullOrWhiteSpace(playerId))
            {
                return FailedAsync<IReadOnlyList<GameSessionRow>>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.PlayerIdRequired
                );
            }

            return this.QueryAsync<IReadOnlyList<GameSessionRow>>(connection =>
                connection
                    .Table<GameSessionRow>()
                    .Where(session => session.PlayerId == playerId)
                    .OrderByDescending(session => session.FinishedAtUtcMs)
                    .ThenBy(session => session.Id)
                    .ToList()
            );
        }

        /// <inheritdoc/>
        public Task<Result<GameSessionRecord, DatabaseError>> ReadSessionAsync(
            string sessionId
        )
        {
            if (string.IsNullOrWhiteSpace(sessionId))
            {
                return FailedAsync<GameSessionRecord>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.SessionIdRequired
                );
            }

            return this.InTransactionAsync(connection =>
            {
                GameSessionRow session = connection.Find<GameSessionRow>(
                    sessionId
                );
                if (session == null)
                {
                    return Failure<GameSessionRecord>(
                        DatabaseErrorCode.NotFound,
                        DatabaseErrorMessages.SessionNotFound(sessionId)
                    );
                }

                return Result<GameSessionRecord, DatabaseError>.Ok(
                    new GameSessionRecord
                    {
                        Session = session,
                        Puzzles = ReadSessionRows<SessionPuzzleStatsRow>(
                            connection,
                            sessionId
                        ),
                        Monsters = ReadSessionRows<SessionMonsterStatsRow>(
                            connection,
                            sessionId
                        ),
                        Items = ReadSessionRows<SessionItemStatsRow>(
                            connection,
                            sessionId
                        ),
                        Furniture = ReadSessionRows<SessionFurniturePoseRow>(
                            connection,
                            sessionId
                        ),
                        RoomCalibration = connection
                            .Table<SessionRoomCalibrationRow>()
                            .Where(row => row.SessionId == sessionId)
                            .FirstOrDefault(),
                    }
                );
            });
        }

        /// <inheritdoc/>
        public Task<Result<Unit, DatabaseError>> SaveSessionAsync(
            GameSessionRecord record
        )
        {
            if (
                record?.Session == null
                || string.IsNullOrWhiteSpace(record.Session.Id)
            )
            {
                return FailedAsync<Unit>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.FinishedSessionRequired
                );
            }

            return this.InTransactionAsync(connection =>
            {
                if (!MatchesSession(record))
                {
                    return Failure<Unit>(
                        DatabaseErrorCode.InvalidInput,
                        DatabaseErrorMessages.MeasurementsMismatch
                    );
                }

                connection.Insert(record.Session);
                connection.InsertAll(record.Puzzles, runInTransaction: false);
                connection.InsertAll(record.Monsters, runInTransaction: false);
                connection.InsertAll(record.Items, runInTransaction: false);
                connection.InsertAll(record.Furniture, runInTransaction: false);
                if (record.RoomCalibration != null)
                {
                    connection.Insert(record.RoomCalibration);
                }

                return Result<Unit, DatabaseError>.Ok(Unit.Value);
            });
        }

        /// <summary>Reads a set of measurements associated with one session.</summary>
        /// <typeparam name="T">The mapped measurement type.</typeparam>
        /// <param name="connection">The connection reading the session snapshot.</param>
        /// <param name="sessionId">The identifier of the session.</param>
        /// <returns>The measured rows for the session.</returns>
        private static IReadOnlyList<T> ReadSessionRows<T>(
            SQLiteConnection connection,
            string sessionId
        )
            where T : SessionStatisticRow, new()
        {
            return connection
                .Table<T>()
                .Where(row => row.SessionId == sessionId)
                .ToList();
        }

        /// <summary>Verifies that all measurements refer to the session being saved.</summary>
        /// <param name="record">The session and measured rows.</param>
        /// <returns>Whether all references are consistent.</returns>
        private static bool MatchesSession(GameSessionRecord record)
        {
            GameSessionRow session = record.Session;
            return MatchesRuleset(record.Puzzles, session)
                && MatchesRuleset(record.Monsters, session)
                && MatchesRuleset(record.Items, session)
                && record.Furniture != null
                && record.Furniture.All(row =>
                    row != null
                    && row.SessionId == session.Id
                    && row.ContentVersionId == session.ContentVersionId
                    && row.RoomId == session.RoomId
                )
                && (
                    record.RoomCalibration == null
                    || record.RoomCalibration.SessionId == session.Id
                );
        }

        /// <summary>Verifies that the measured rows belong to the session and its ruleset.</summary>
        /// <param name="rows">The statistics to verify.</param>
        /// <param name="session">The owning session.</param>
        /// <returns>Whether all references match the owning session.</returns>
        private static bool MatchesRuleset(
            IEnumerable<RulesetStatisticRow> rows,
            GameSessionRow session
        )
        {
            return rows != null
                && rows.All(row =>
                    row != null
                    && row.SessionId == session.Id
                    && row.ContentVersionId == session.ContentVersionId
                    && row.RulesetId == session.RulesetId
                );
        }
    }
}
