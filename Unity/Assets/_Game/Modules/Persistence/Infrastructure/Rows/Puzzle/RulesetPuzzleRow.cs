namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ruleset_puzzles relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ruleset_puzzles")]
    public sealed class RulesetPuzzleRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the scenario id.</summary>
        [Column("scenario_id")]
        public string ScenarioId { get; set; }

        /// <summary>Gets or sets the puzzle id.</summary>
        [Column("puzzle_id")]
        public string PuzzleId { get; set; }

        /// <summary>Gets or sets the variant id.</summary>
        [Column("variant_id")]
        public string VariantId { get; set; }

        /// <summary>Gets or sets the display order.</summary>
        [Column("display_order")]
        public long DisplayOrder { get; set; }

        /// <summary>Gets or sets the required for exit.</summary>
        [Column("required_for_exit")]
        public long RequiredForExit { get; set; }
    }
}
