namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_profiles relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_profiles")]
    public sealed class MonsterProfileRow : VersionedRow
    {
        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the difficulty id.</summary>
        [Column("difficulty_id")]
        public string DifficultyId { get; set; }

        /// <summary>Gets or sets the allows monster.</summary>
        [Column("allows_monster")]
        public long AllowsMonster { get; set; }

        /// <summary>Gets or sets the vision fov deg.</summary>
        [Column("vision_fov_deg")]
        public double VisionFovDeg { get; set; }

        /// <summary>Gets or sets the investigate distance m.</summary>
        [Column("investigate_distance_m")]
        public double InvestigateDistanceM { get; set; }

        /// <summary>Gets or sets the chase distance m.</summary>
        [Column("chase_distance_m")]
        public double ChaseDistanceM { get; set; }

        /// <summary>Gets or sets the attack distance m.</summary>
        [Column("attack_distance_m")]
        public double AttackDistanceM { get; set; }

        /// <summary>Gets or sets the vision acquire ms.</summary>
        [Column("vision_acquire_ms")]
        public long VisionAcquireMs { get; set; }

        /// <summary>Gets or sets the vision lose ms.</summary>
        [Column("vision_lose_ms")]
        public long VisionLoseMs { get; set; }

        /// <summary>Gets or sets the hearing range m.</summary>
        [Column("hearing_range_m")]
        public double HearingRangeM { get; set; }

        /// <summary>Gets or sets the hearing threshold.</summary>
        [Column("hearing_threshold")]
        public double HearingThreshold { get; set; }

        /// <summary>Gets or sets the visual memory ms.</summary>
        [Column("visual_memory_ms")]
        public long VisualMemoryMs { get; set; }

        /// <summary>Gets or sets the noise memory ms.</summary>
        [Column("noise_memory_ms")]
        public long NoiseMemoryMs { get; set; }

        /// <summary>Gets or sets the investigate duration ms.</summary>
        [Column("investigate_duration_ms")]
        public long InvestigateDurationMs { get; set; }

        /// <summary>Gets or sets the investigate distance estimate m.</summary>
        [Column("investigate_distance_estimate_m")]
        public double InvestigateDistanceEstimateM { get; set; }

        /// <summary>Gets or sets the search duration ms.</summary>
        [Column("search_duration_ms")]
        public long SearchDurationMs { get; set; }

        /// <summary>Gets or sets the search radius m.</summary>
        [Column("search_radius_m")]
        public double SearchRadiusM { get; set; }

        /// <summary>Gets or sets the chase persistence ms.</summary>
        [Column("chase_persistence_ms")]
        public long ChasePersistenceMs { get; set; }

        /// <summary>Gets or sets the patrol speed mps.</summary>
        [Column("patrol_speed_mps")]
        public double PatrolSpeedMps { get; set; }

        /// <summary>Gets or sets the investigate speed mps.</summary>
        [Column("investigate_speed_mps")]
        public double InvestigateSpeedMps { get; set; }

        /// <summary>Gets or sets the search speed mps.</summary>
        [Column("search_speed_mps")]
        public double SearchSpeedMps { get; set; }

        /// <summary>Gets or sets the chase speed mps.</summary>
        [Column("chase_speed_mps")]
        public double ChaseSpeedMps { get; set; }

        /// <summary>Gets or sets the attack cooldown ms.</summary>
        [Column("attack_cooldown_ms")]
        public long AttackCooldownMs { get; set; }

        /// <summary>Gets or sets the recovery duration ms.</summary>
        [Column("recovery_duration_ms")]
        public long RecoveryDurationMs { get; set; }

        /// <summary>Gets or sets the impact threshold multiplier.</summary>
        [Column("impact_threshold_multiplier")]
        public double ImpactThresholdMultiplier { get; set; }

        /// <summary>Gets or sets the slow speed multiplier.</summary>
        [Column("slow_speed_multiplier")]
        public double SlowSpeedMultiplier { get; set; }

        /// <summary>Gets or sets the slow duration multiplier.</summary>
        [Column("slow_duration_multiplier")]
        public double SlowDurationMultiplier { get; set; }

        /// <summary>Gets or sets the stun duration multiplier.</summary>
        [Column("stun_duration_multiplier")]
        public double StunDurationMultiplier { get; set; }
    }
}
