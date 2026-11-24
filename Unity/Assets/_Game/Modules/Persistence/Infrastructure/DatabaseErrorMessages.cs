namespace Project.Persistence
{
    /// <summary>Contains the messages returned by the database interface.</summary>
    internal static class DatabaseErrorMessages
    {
        /// <summary>Message for an empty database path.</summary>
        internal const string DatabasePathRequired =
            "A database path is required.";

        /// <summary>Message for missing initialization scripts.</summary>
        internal const string SchemaResourcesMissing =
            "The packaged database schema or initial catalog is unavailable.";

        /// <summary>Message for an empty player name.</summary>
        internal const string PlayerNameRequired = "A player name is required.";

        /// <summary>Message for an empty player identifier.</summary>
        internal const string PlayerIdRequired = "A player ID is required.";

        /// <summary>Message for an incomplete request to rename a player.</summary>
        internal const string PlayerIdAndNameRequired =
            "A player ID and name are required.";

        /// <summary>Message for invalid leaderboard filters or limits.</summary>
        internal const string InvalidLeaderboardRequest =
            "A content version, a ruleset and a positive leaderboard limit are required.";

        /// <summary>Message for an empty catalog version identifier.</summary>
        internal const string CatalogVersionRequired =
            "A catalog version ID is required.";

        /// <summary>Message for the absence of an active catalog.</summary>
        internal const string ActiveCatalogNotFound =
            "No catalog version is active.";

        /// <summary>Message for an empty session identifier.</summary>
        internal const string SessionIdRequired = "A session ID is required.";

        /// <summary>Message for a missing session or session identifier on save.</summary>
        internal const string FinishedSessionRequired =
            "A finished session with an ID is required.";

        /// <summary>Message for measurements referring to a different session.</summary>
        internal const string MeasurementsMismatch =
            "All measurements must belong to the finished session.";

        /// <summary>Formats the message for an unsupported schema version.</summary>
        /// <param name="version">The stored schema version.</param>
        /// <returns>The error message.</returns>
        internal static string UnsupportedSchema(int version)
        {
            return $"Unsupported Tohannic database schema version {version}.";
        }

        /// <summary>Formats the message for a missing player.</summary>
        /// <param name="playerId">The requested player identifier.</param>
        /// <returns>The error message.</returns>
        internal static string PlayerNotFound(string playerId)
        {
            return $"Player '{playerId}' was not found.";
        }

        /// <summary>Formats the message for a missing catalog version.</summary>
        /// <param name="versionId">The requested catalog version identifier.</param>
        /// <returns>The error message.</returns>
        internal static string CatalogVersionNotFound(string versionId)
        {
            return $"Catalog version '{versionId}' was not found.";
        }

        /// <summary>Formats the message for a missing session.</summary>
        /// <param name="sessionId">The requested session identifier.</param>
        /// <returns>The error message.</returns>
        internal static string SessionNotFound(string sessionId)
        {
            return $"Session '{sessionId}' was not found.";
        }

        /// <summary>Selects a message for a failed SQLite or file system operation.</summary>
        /// <param name="code">The error code determined from the failure.</param>
        /// <returns>The error message.</returns>
        internal static string ForOperationFailure(DatabaseErrorCode code)
        {
            return code switch
            {
                DatabaseErrorCode.InvalidInput =>
                    "A database argument is invalid.",
                DatabaseErrorCode.Busy =>
                    "The database is busy. Please try again.",
                DatabaseErrorCode.Constraint =>
                    "The database rejected the supplied data.",
                _ => "The database operation did not complete.",
            };
        }
    }
}
