namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_steps relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_steps")]
    public sealed class PuzzleStepRow : VersionedRow
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

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the instruction.</summary>
        [Column("instruction")]
        public string Instruction { get; set; }
    }
}
