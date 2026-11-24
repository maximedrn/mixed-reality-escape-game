namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the items relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("items")]
    public sealed class ItemRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the prefab asset id.</summary>
        [Column("prefab_asset_id")]
        public string PrefabAssetId { get; set; }

        /// <summary>Gets or sets the mass kg.</summary>
        [Column("mass_kg")]
        public double? MassKg { get; set; }

        /// <summary>Gets or sets the break speed mps.</summary>
        [Column("break_speed_mps")]
        public double? BreakSpeedMps { get; set; }

        /// <summary>Gets or sets the impact audio asset id.</summary>
        [Column("impact_audio_asset_id")]
        public string ImpactAudioAssetId { get; set; }

        /// <summary>Gets or sets the break audio asset id.</summary>
        [Column("break_audio_asset_id")]
        public string BreakAudioAssetId { get; set; }
    }
}
