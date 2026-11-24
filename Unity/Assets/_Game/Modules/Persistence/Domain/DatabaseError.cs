namespace Project.Persistence
{
    /// <summary>Describes a failed database operation.</summary>
    public readonly struct DatabaseError
    {
        /// <summary>Initializes a new instance of the <see cref="DatabaseError"/> struct.</summary>
        /// <param name="code">The kind of database failure.</param>
        /// <param name="message">The message shown to the player.</param>
        public DatabaseError(DatabaseErrorCode code, string message)
        {
            this.Code = code;
            this.Message = message;
            this.TechnicalDetails = null;
        }

        /// <summary>Initializes a new instance of the <see cref="DatabaseError"/> struct.</summary>
        /// <param name="code">The kind of database failure.</param>
        /// <param name="message">The message shown to the player.</param>
        /// <param name="technicalDetails">Optional diagnostic information from the database.</param>
        internal DatabaseError(
            DatabaseErrorCode code,
            string message,
            string technicalDetails
        )
            : this(code, message)
        {
            this.TechnicalDetails = technicalDetails;
        }

        /// <summary>Gets the kind of database failure.</summary>
        public DatabaseErrorCode Code { get; }

        /// <summary>Gets the message shown to the player.</summary>
        public string Message { get; }

        /// <summary>Gets the optional diagnostic information from the database.</summary>
        public string TechnicalDetails { get; }
    }
}
