namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the game_sessions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("game_sessions")]
    public sealed class GameSessionRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the player id.</summary>
        [Column("player_id")]
        public string PlayerId { get; set; }

        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the started at utc ms.</summary>
        [Column("started_at_utc_ms")]
        public long StartedAtUtcMs { get; set; }

        /// <summary>Gets or sets the finished at utc ms.</summary>
        [Column("finished_at_utc_ms")]
        public long FinishedAtUtcMs { get; set; }

        /// <summary>Gets or sets the duration ms.</summary>
        [Column("duration_ms")]
        public long DurationMs { get; set; }

        /// <summary>Gets or sets the outcome.</summary>
        [Column("outcome")]
        public string Outcome { get; set; }

        /// <summary>Gets or sets the leaderboard eligible.</summary>
        [Column("leaderboard_eligible")]
        public long LeaderboardEligible { get; set; }
    }
}
