namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ruleset_puzzle_prerequisites relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ruleset_puzzle_prerequisites")]
    public sealed class RulesetPuzzlePrerequisiteRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the puzzle id.</summary>
        [Column("puzzle_id")]
        public string PuzzleId { get; set; }

        /// <summary>Gets or sets the required puzzle id.</summary>
        [Column("required_puzzle_id")]
        public string RequiredPuzzleId { get; set; }
    }
}
