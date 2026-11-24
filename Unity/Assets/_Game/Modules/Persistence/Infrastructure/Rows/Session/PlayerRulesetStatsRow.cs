namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the player_ruleset_stats relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("player_ruleset_stats")]
    public sealed class PlayerRulesetStatsRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the player id.</summary>
        [Column("player_id")]
        public string PlayerId { get; set; }

        /// <summary>Gets or sets the sessions played.</summary>
        [Column("sessions_played")]
        public long SessionsPlayed { get; set; }

        /// <summary>Gets or sets the wins.</summary>
        [Column("wins")]
        public long Wins { get; set; }

        /// <summary>Gets or sets the losses.</summary>
        [Column("losses")]
        public long Losses { get; set; }

        /// <summary>Gets or sets the best win duration ms.</summary>
        [Column("best_win_duration_ms")]
        public long? BestWinDurationMs { get; set; }
    }
}
