namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the content_versions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("content_versions")]
    public sealed class ContentVersionRow
    {
        /// <summary>Gets or sets the id.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the created at utc ms.</summary>
        [Column("created_at_utc_ms")]
        public long CreatedAtUtcMs { get; set; }
    }
}
