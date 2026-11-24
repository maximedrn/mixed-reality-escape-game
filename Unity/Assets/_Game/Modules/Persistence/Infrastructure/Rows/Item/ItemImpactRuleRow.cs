namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_impact_rules relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_impact_rules")]
    public sealed class ItemImpactRuleRow : VersionedRow
    {
        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the effect id.</summary>
        [Column("effect_id")]
        public string EffectId { get; set; }

        /// <summary>Gets or sets the min strength kg mps.</summary>
        [Column("min_strength_kg_mps")]
        public double MinStrengthKgMps { get; set; }

        /// <summary>Gets or sets the base duration ms.</summary>
        [Column("base_duration_ms")]
        public long? BaseDurationMs { get; set; }
    }
}
