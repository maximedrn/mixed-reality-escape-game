namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps the content version shared by catalog rows.</summary>
    public abstract class VersionedRow
    {
        /// <summary>Gets or sets the content version id.</summary>
        [Column("content_version_id")]
        public string ContentVersionId { get; set; }
    }
}
