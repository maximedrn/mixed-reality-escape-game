namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the session_monster_stats relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("session_monster_stats")]
    public sealed class SessionMonsterStatsRow : RulesetStatisticRow
    {
        /// <summary>Gets or sets the spawn id.</summary>
        [Column("spawn_id")]
        public string SpawnId { get; set; }

        /// <summary>Gets or sets the confirmed detections.</summary>
        [Column("confirmed_detections")]
        public long ConfirmedDetections { get; set; }

        /// <summary>Gets or sets the noises perceived.</summary>
        [Column("noises_perceived")]
        public long NoisesPerceived { get; set; }

        /// <summary>Gets or sets the chases.</summary>
        [Column("chases")]
        public long Chases { get; set; }

        /// <summary>Gets or sets the attacks.</summary>
        [Column("attacks")]
        public long Attacks { get; set; }

        /// <summary>Gets or sets the stuns.</summary>
        [Column("stuns")]
        public long Stuns { get; set; }
    }
}
