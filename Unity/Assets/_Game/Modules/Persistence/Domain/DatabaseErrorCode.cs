namespace Project.Persistence
{
    /// <summary>Identifies expected failures of a database operation.</summary>
    public enum DatabaseErrorCode
    {
        /// <summary>The caller supplied an invalid input.</summary>
        InvalidInput,

        /// <summary>The requested data or active catalog does not exist.</summary>
        NotFound,

        /// <summary>The database was created with a different schema version.</summary>
        UnsupportedSchema,

        /// <summary>A packaged SQL resource is unavailable.</summary>
        MissingResource,

        /// <summary>Another connection holds a lock needed by the operation.</summary>
        Busy,

        /// <summary>SQLite rejected a write that violates a constraint.</summary>
        Constraint,

        /// <summary>The storage operation could not be completed.</summary>
        Storage,
    }
}
