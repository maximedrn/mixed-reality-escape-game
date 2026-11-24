namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monsters relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monsters")]
    public sealed class MonsterRow : VersionedRow
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

        /// <summary>Gets or sets the animator asset id.</summary>
        [Column("animator_asset_id")]
        public string AnimatorAssetId { get; set; }

        /// <summary>Gets or sets the attack range m.</summary>
        [Column("attack_range_m")]
        public double? AttackRangeM { get; set; }

        /// <summary>Gets or sets the nav agent radius m.</summary>
        [Column("nav_agent_radius_m")]
        public double? NavAgentRadiusM { get; set; }

        /// <summary>Gets or sets the nav agent height m.</summary>
        [Column("nav_agent_height_m")]
        public double? NavAgentHeightM { get; set; }
    }
}
