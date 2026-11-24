namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a read-only result from the leaderboard_entries view.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("leaderboard_entries")]
    public sealed class LeaderboardEntryRow
    {
        /// <summary>Gets or sets the published version used to play the session.</summary>
        [Column("content_version_id")]
        public string ContentVersionId { get; set; }

        /// <summary>Gets or sets the ruleset identifier.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the player's position on the leaderboard.</summary>
        [Column("rank")]
        public long Rank { get; set; }

        /// <summary>Gets or sets the identifier of the ranked player.</summary>
        [Column("player_id")]
        public string PlayerId { get; set; }

        /// <summary>Gets or sets the player's current display name.</summary>
        [Column("display_name")]
        public string DisplayName { get; set; }

        /// <summary>Gets or sets the identifier of the ranked session.</summary>
        [Column("session_id")]
        public string SessionId { get; set; }

        /// <summary>Gets or sets the winning elapsed time in milliseconds.</summary>
        [Column("duration_ms")]
        public long DurationMs { get; set; }

        /// <summary>Gets or sets the completion timestamp in Unix milliseconds.</summary>
        [Column("finished_at_utc_ms")]
        public long FinishedAtUtcMs { get; set; }
    }
}
