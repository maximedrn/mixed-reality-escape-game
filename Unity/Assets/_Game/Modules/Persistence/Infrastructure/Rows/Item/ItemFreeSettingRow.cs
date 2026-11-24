namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_free_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_free_settings")]
    public sealed class ItemFreeSettingRow : VersionedRow
    {
        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the point id.</summary>
        [Column("point_id")]
        public string PointId { get; set; }

        /// <summary>Gets or sets the kind id.</summary>
        [Column("kind_id")]
        public string KindId { get; set; }

        /// <summary>Gets or sets the max translation m.</summary>
        [Column("max_translation_m")]
        public double? MaxTranslationM { get; set; }

        /// <summary>Gets or sets the max rotation deg.</summary>
        [Column("max_rotation_deg")]
        public double? MaxRotationDeg { get; set; }
    }
}
