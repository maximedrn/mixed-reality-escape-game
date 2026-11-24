namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_animation_bindings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_animation_bindings")]
    public sealed class MonsterAnimationBindingRow : VersionedRow
    {
        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the action.</summary>
        [Column("action")]
        public string Action { get; set; }

        /// <summary>Gets or sets the slot.</summary>
        [Column("slot")]
        public long Slot { get; set; }

        /// <summary>Gets or sets the clip id.</summary>
        [Column("clip_id")]
        public string ClipId { get; set; }

        /// <summary>Gets or sets the playback speed.</summary>
        [Column("playback_speed")]
        public double PlaybackSpeed { get; set; }

        /// <summary>Gets or sets the finish timeout ms.</summary>
        [Column("finish_timeout_ms")]
        public long? FinishTimeoutMs { get; set; }
    }
}
