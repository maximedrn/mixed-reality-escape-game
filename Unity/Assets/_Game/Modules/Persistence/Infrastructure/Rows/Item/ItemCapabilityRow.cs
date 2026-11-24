namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_capabilities relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_capabilities")]
    public sealed class ItemCapabilityRow : VersionedRow
    {
        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the capability id.</summary>
        [Column("capability_id")]
        public string CapabilityId { get; set; }
    }
}
