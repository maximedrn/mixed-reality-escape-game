namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the session_puzzle_stats relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("session_puzzle_stats")]
    public sealed class SessionPuzzleStatsRow : RulesetStatisticRow
    {
        /// <summary>Gets or sets the puzzle id.</summary>
        [Column("puzzle_id")]
        public string PuzzleId { get; set; }

        /// <summary>Gets or sets the attempt count.</summary>
        [Column("attempt_count")]
        public long AttemptCount { get; set; }

        /// <summary>Gets or sets the hints used.</summary>
        [Column("hints_used")]
        public long HintsUsed { get; set; }

        /// <summary>Gets or sets the available at elapsed ms.</summary>
        [Column("available_at_elapsed_ms")]
        public long? AvailableAtElapsedMs { get; set; }

        /// <summary>Gets or sets the solved at elapsed ms.</summary>
        [Column("solved_at_elapsed_ms")]
        public long? SolvedAtElapsedMs { get; set; }
    }
}
