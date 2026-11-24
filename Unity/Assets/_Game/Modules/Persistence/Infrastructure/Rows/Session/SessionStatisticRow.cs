namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps the session identity shared by subordinate records.</summary>
    public abstract class SessionStatisticRow
    {
        /// <summary>Gets or sets the session id.</summary>
        [Column("session_id")]
        public string SessionId { get; set; }
    }
}
