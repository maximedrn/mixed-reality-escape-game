namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_assembly_conditions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_assembly_conditions")]
    public sealed class PuzzleAssemblyConditionRow : VersionedRow
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

        /// <summary>Gets or sets the condition number.</summary>
        [Column("condition_number")]
        public long ConditionNumber { get; set; }

        /// <summary>Gets or sets the kind.</summary>
        [Column("kind")]
        public string Kind { get; set; }

        /// <summary>Gets or sets the first placement id.</summary>
        [Column("first_placement_id")]
        public string FirstPlacementId { get; set; }

        /// <summary>Gets or sets the second placement id.</summary>
        [Column("second_placement_id")]
        public string SecondPlacementId { get; set; }

        /// <summary>Gets or sets the position tolerance m.</summary>
        [Column("position_tolerance_m")]
        public double PositionToleranceM { get; set; }

        /// <summary>Gets or sets the rotation tolerance deg.</summary>
        [Column("rotation_tolerance_deg")]
        public double RotationToleranceDeg { get; set; }
    }
}
