namespace Project.Persistence
{
    using System.Collections.Generic;
    using System.Threading.Tasks;
    using Project.Core;

    /// <summary>Provides typed access to the game's saved data and configuration.</summary>
    public interface IGameDatabase
    {
        /// <summary>Creates a local player.</summary>
        /// <param name="displayName">The name visible in the game.</param>
        /// <returns>The stored player or a database error.</returns>
        Task<Result<PlayerRow, DatabaseError>> AddPlayerAsync(
            string displayName
        );

        /// <summary>Reads a player by stable identity.</summary>
        /// <param name="playerId">The identifier of the player.</param>
        /// <returns>The player or a database error.</returns>
        Task<Result<PlayerRow, DatabaseError>> ReadPlayerAsync(string playerId);

        /// <summary>Reads the local player profiles ordered by display name.</summary>
        /// <returns>The player profiles or a database error.</returns>
        Task<
            Result<IReadOnlyList<PlayerRow>, DatabaseError>
        > ReadPlayersAsync();

        /// <summary>Updates a player's display name.</summary>
        /// <param name="playerId">The stable identity of the player.</param>
        /// <param name="displayName">The replacement display name.</param>
        /// <returns>The updated player or a database error.</returns>
        Task<Result<PlayerRow, DatabaseError>> RenamePlayerAsync(
            string playerId,
            string displayName
        );

        /// <summary>Reads the best ranked victory of each player for a ruleset version.</summary>
        /// <param name="contentVersionId">The identifier of the content version scored.</param>
        /// <param name="rulesetId">The ruleset used to group results.</param>
        /// <param name="limit">The maximum number of ranked entries to return.</param>
        /// <returns>The entries in rank order or a database error.</returns>
        Task<
            Result<IReadOnlyList<LeaderboardEntryRow>, DatabaseError>
        > ReadLeaderboardAsync(
            string contentVersionId,
            string rulesetId,
            int limit
        );

        /// <summary>Reads aggregated results for each ruleset a player has played.</summary>
        /// <param name="playerId">The identifier of the player.</param>
        /// <returns>The win and loss summaries or a database error.</returns>
        Task<
            Result<IReadOnlyList<PlayerRulesetStatsRow>, DatabaseError>
        > ReadPlayerStatsAsync(string playerId);

        /// <summary>Reads a player's completed sessions, starting with the most recent.</summary>
        /// <param name="playerId">The identifier of the player.</param>
        /// <returns>The session summaries or a database error.</returns>
        Task<
            Result<IReadOnlyList<GameSessionRow>, DatabaseError>
        > ReadSessionsAsync(string playerId);

        /// <summary>Reads a completed session with its recorded statistics.</summary>
        /// <param name="sessionId">The identifier of the session.</param>
        /// <returns>The complete session or a database error.</returns>
        Task<Result<GameSessionRecord, DatabaseError>> ReadSessionAsync(
            string sessionId
        );

        /// <summary>Stores a completed session and its statistics atomically.</summary>
        /// <param name="record">The session and associated measurements.</param>
        /// <returns>The result of saving the session.</returns>
        Task<Result<Unit, DatabaseError>> SaveSessionAsync(
            GameSessionRecord record
        );

        /// <summary>Reads an entire configuration at a specified version.</summary>
        /// <param name="contentVersionId">The requested catalog version.</param>
        /// <returns>The catalog or a database error.</returns>
        Task<Result<GameCatalog, DatabaseError>> ReadCatalogAsync(
            string contentVersionId
        );

        /// <summary>Reads the configuration published for new sessions.</summary>
        /// <returns>The active catalog or a database error.</returns>
        Task<Result<GameCatalog, DatabaseError>> ReadActiveCatalogAsync();
    }
}
