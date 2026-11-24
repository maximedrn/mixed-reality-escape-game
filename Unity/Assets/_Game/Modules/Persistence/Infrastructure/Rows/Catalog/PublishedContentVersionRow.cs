namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the published_content_versions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("published_content_versions")]
    public sealed class PublishedContentVersionRow
    {
        /// <summary>Gets or sets the content version id.</summary>
        [PrimaryKey]
        [Column("content_version_id")]
        public string ContentVersionId { get; set; }

        /// <summary>Gets or sets the published at utc ms.</summary>
        [Column("published_at_utc_ms")]
        public long PublishedAtUtcMs { get; set; }
    }
}
