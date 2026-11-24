namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_interaction_points relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_interaction_points")]
    public sealed class ItemInteractionPointRow : VersionedRow
    {
        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the kind id.</summary>
        [Column("kind_id")]
        public string KindId { get; set; }

        /// <summary>Gets or sets the prefab binding.</summary>
        [Column("prefab_binding")]
        public string PrefabBinding { get; set; }

        /// <summary>Gets or sets the proximity m.</summary>
        [Column("proximity_m")]
        public double? ProximityM { get; set; }
    }
}
