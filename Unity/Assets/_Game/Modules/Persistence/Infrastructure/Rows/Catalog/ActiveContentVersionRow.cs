namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the active_content_version relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("active_content_version")]
    internal sealed class ActiveContentVersionRow
    {
        /// <summary>Gets or sets the slot.</summary>
        [PrimaryKey]
        [Column("slot")]
        public long Slot { get; set; }

        /// <summary>Gets or sets the content version id.</summary>
        [Column("content_version_id")]
        public string ContentVersionId { get; set; }
    }
}
