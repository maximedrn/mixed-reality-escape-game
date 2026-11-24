namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_hints relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_hints")]
    public sealed class PuzzleHintRow : VersionedRow
    {
        /// <summary>Gets or sets the scenario id.</summary>
        [Column("scenario_id")]
        public string ScenarioId { get; set; }

        /// <summary>Gets or sets the variant id.</summary>
        [Column("variant_id")]
        public string VariantId { get; set; }

        /// <summary>Gets or sets the step number.</summary>
        [Column("step_number")]
        public long StepNumber { get; set; }

        /// <summary>Gets or sets the hint number.</summary>
        [Column("hint_number")]
        public long HintNumber { get; set; }

        /// <summary>Gets or sets the message.</summary>
        [Column("message")]
        public string Message { get; set; }

        /// <summary>Gets or sets the available after ms.</summary>
        [Column("available_after_ms")]
        public long AvailableAfterMs { get; set; }
    }
}
