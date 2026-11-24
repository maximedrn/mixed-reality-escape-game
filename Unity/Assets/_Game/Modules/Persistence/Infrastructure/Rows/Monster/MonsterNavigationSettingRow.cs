namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_navigation_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_navigation_settings")]
    public sealed class MonsterNavigationSettingRow : VersionedRow
    {
        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the projection tolerance m.</summary>
        [Column("projection_tolerance_m")]
        public double ProjectionToleranceM { get; set; }

        /// <summary>Gets or sets the adjacency tolerance m.</summary>
        [Column("adjacency_tolerance_m")]
        public double AdjacencyToleranceM { get; set; }

        /// <summary>Gets or sets the repath interval ms.</summary>
        [Column("repath_interval_ms")]
        public long RepathIntervalMs { get; set; }

        /// <summary>Gets or sets the target move threshold m.</summary>
        [Column("target_move_threshold_m")]
        public double TargetMoveThresholdM { get; set; }
    }
}
