namespace Project.Persistence
{
    using System;
    using System.Collections.Generic;
    using System.Threading.Tasks;
    using Project.Core;
    using SQLite;

    public sealed partial class GameDatabase
    {
        /// <inheritdoc/>
        public Task<Result<PlayerRow, DatabaseError>> AddPlayerAsync(
            string displayName
        )
        {
            if (string.IsNullOrWhiteSpace(displayName))
            {
                return FailedAsync<PlayerRow>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.PlayerNameRequired
                );
            }

            return this.QueryAsync(connection =>
            {
                PlayerRow player = new PlayerRow
                {
                    Id = Guid.NewGuid().ToString("D"),
                    DisplayName = displayName.Trim(),
                    CreatedAtUtcMs =
                        DateTimeOffset.UtcNow.ToUnixTimeMilliseconds(),
                };
                connection.Insert(player);
                return player;
            });
        }

        /// <inheritdoc/>
        public Task<Result<PlayerRow, DatabaseError>> ReadPlayerAsync(
            string playerId
        )
        {
            if (string.IsNullOrWhiteSpace(playerId))
            {
                return FailedAsync<PlayerRow>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.PlayerIdRequired
                );
            }

            return this.WithConnectionAsync(connection =>
                FindPlayer(connection, playerId)
            );
        }

        /// <inheritdoc/>
        public Task<
            Result<IReadOnlyList<PlayerRow>, DatabaseError>
        > ReadPlayersAsync()
        {
            return this.QueryAsync<IReadOnlyList<PlayerRow>>(connection =>
                connection
                    .Table<PlayerRow>()
                    .OrderBy(player => player.DisplayName)
                    .ThenBy(player => player.Id)
                    .ToList()
            );
        }

        /// <inheritdoc/>
        public Task<Result<PlayerRow, DatabaseError>> RenamePlayerAsync(
            string playerId,
            string displayName
        )
        {
            if (
                string.IsNullOrWhiteSpace(playerId)
                || string.IsNullOrWhiteSpace(displayName)
            )
            {
                return FailedAsync<PlayerRow>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.PlayerIdAndNameRequired
                );
            }

            return this.InTransactionAsync(connection =>
            {
                Result<PlayerRow, DatabaseError> result = FindPlayer(
                    connection,
                    playerId
                );
                if (result.TryGetValue(out PlayerRow player))
                {
                    player.DisplayName = displayName.Trim();
                    connection.Update(player);
                }

                return result;
            });
        }

        /// <inheritdoc/>
        public Task<
            Result<IReadOnlyList<LeaderboardEntryRow>, DatabaseError>
        > ReadLeaderboardAsync(
            string contentVersionId,
            string rulesetId,
            int limit
        )
        {
            if (
                string.IsNullOrWhiteSpace(contentVersionId)
                || string.IsNullOrWhiteSpace(rulesetId)
                || limit < 1
            )
            {
                return FailedAsync<IReadOnlyList<LeaderboardEntryRow>>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.InvalidLeaderboardRequest
                );
            }

            return this.QueryAsync<IReadOnlyList<LeaderboardEntryRow>>(
                connection =>
                    connection
                        .Table<LeaderboardEntryRow>()
                        .Where(entry =>
                            entry.ContentVersionId == contentVersionId
                            && entry.RulesetId == rulesetId
                        )
                        .OrderBy(entry => entry.Rank)
                        .Take(limit)
                        .ToList()
            );
        }

        /// <inheritdoc/>
        public Task<
            Result<IReadOnlyList<PlayerRulesetStatsRow>, DatabaseError>
        > ReadPlayerStatsAsync(string playerId)
        {
            if (string.IsNullOrWhiteSpace(playerId))
            {
                return FailedAsync<IReadOnlyList<PlayerRulesetStatsRow>>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.PlayerIdRequired
                );
            }

            return this.QueryAsync<IReadOnlyList<PlayerRulesetStatsRow>>(
                connection =>
                    connection
                        .Table<PlayerRulesetStatsRow>()
                        .Where(stats => stats.PlayerId == playerId)
                        .OrderBy(stats => stats.ContentVersionId)
                        .ThenBy(stats => stats.RulesetId)
                        .ToList()
            );
        }

        /// <inheritdoc/>
        public Task<Result<GameCatalog, DatabaseError>> ReadCatalogAsync(
            string contentVersionId
        )
        {
            if (string.IsNullOrWhiteSpace(contentVersionId))
            {
                return FailedAsync<GameCatalog>(
                    DatabaseErrorCode.InvalidInput,
                    DatabaseErrorMessages.CatalogVersionRequired
                );
            }

            return this.InTransactionAsync(connection =>
                FindCatalog(connection, contentVersionId)
            );
        }

        /// <inheritdoc/>
        public Task<Result<GameCatalog, DatabaseError>> ReadActiveCatalogAsync()
        {
            return this.InTransactionAsync(connection =>
            {
                ActiveContentVersionRow active = connection
                    .Table<ActiveContentVersionRow>()
                    .FirstOrDefault();
                if (active == null)
                {
                    return Failure<GameCatalog>(
                        DatabaseErrorCode.NotFound,
                        DatabaseErrorMessages.ActiveCatalogNotFound
                    );
                }

                return FindCatalog(connection, active.ContentVersionId);
            });
        }

        /// <summary>Reads a player's row or reports that the identifier is unknown.</summary>
        /// <param name="connection">The connection reading the player.</param>
        /// <param name="playerId">The stable identity of the player.</param>
        /// <returns>The requested player or a database error.</returns>
        private static Result<PlayerRow, DatabaseError> FindPlayer(
            SQLiteConnection connection,
            string playerId
        )
        {
            PlayerRow player = connection.Find<PlayerRow>(playerId);
            if (player == null)
            {
                return Failure<PlayerRow>(
                    DatabaseErrorCode.NotFound,
                    DatabaseErrorMessages.PlayerNotFound(playerId)
                );
            }

            return Result<PlayerRow, DatabaseError>.Ok(player);
        }

        /// <summary>Reads a specific version and the rows belonging to it.</summary>
        /// <param name="connection">The connection reading the catalog snapshot.</param>
        /// <param name="versionId">The requested content version.</param>
        /// <returns>The requested catalog or a database error.</returns>
        private static Result<GameCatalog, DatabaseError> FindCatalog(
            SQLiteConnection connection,
            string versionId
        )
        {
            ContentVersionRow version = connection.Find<ContentVersionRow>(
                versionId
            );
            if (version == null)
            {
                return Failure<GameCatalog>(
                    DatabaseErrorCode.NotFound,
                    DatabaseErrorMessages.CatalogVersionNotFound(versionId)
                );
            }

            return Result<GameCatalog, DatabaseError>.Ok(
                new GameCatalog(connection, version)
            );
        }

        /// <summary>Runs a group of reads or writes in one database transaction.</summary>
        /// <typeparam name="T">The successful value type.</typeparam>
        /// <param name="operation">The database work within the transaction.</param>
        /// <returns>The asynchronous result of the operation.</returns>
        private Task<Result<T, DatabaseError>> InTransactionAsync<T>(
            Func<SQLiteConnection, Result<T, DatabaseError>> operation
        )
        {
            return this.WithConnectionAsync(connection =>
            {
                Result<T, DatabaseError> result = default(Result<
                    T,
                    DatabaseError
                >);
                connection.RunInTransaction(() =>
                    result = operation(connection)
                );
                return result;
            });
        }
    }
}
