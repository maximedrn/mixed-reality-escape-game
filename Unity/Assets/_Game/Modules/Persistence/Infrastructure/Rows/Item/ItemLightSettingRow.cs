namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_light_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_light_settings")]
    public sealed class ItemLightSettingRow : VersionedRow
    {
        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the intensity.</summary>
        [Column("intensity")]
        public double Intensity { get; set; }

        /// <summary>Gets or sets the range m.</summary>
        [Column("range_m")]
        public double RangeM { get; set; }

        /// <summary>Gets or sets the red.</summary>
        [Column("red")]
        public double Red { get; set; }

        /// <summary>Gets or sets the green.</summary>
        [Column("green")]
        public double Green { get; set; }

        /// <summary>Gets or sets the blue.</summary>
        [Column("blue")]
        public double Blue { get; set; }

        /// <summary>Gets or sets the initially on.</summary>
        [Column("initially_on")]
        public long InitiallyOn { get; set; }
    }
}
