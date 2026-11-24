namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_capability_kinds relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_capability_kinds")]
    public sealed class ItemCapabilityKindRow
    {
        /// <summary>Gets or sets the id.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }
    }
}
