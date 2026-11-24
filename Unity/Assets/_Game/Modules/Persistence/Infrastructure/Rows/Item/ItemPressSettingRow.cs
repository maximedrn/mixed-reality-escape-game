namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_press_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_press_settings")]
    public sealed class ItemPressSettingRow : VersionedRow
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

        /// <summary>Gets or sets the allow pinch.</summary>
        [Column("allow_pinch")]
        public long AllowPinch { get; set; }
    }
}
