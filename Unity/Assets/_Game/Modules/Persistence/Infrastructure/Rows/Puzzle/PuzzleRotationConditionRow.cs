namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_rotation_conditions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_rotation_conditions")]
    public sealed class PuzzleRotationConditionRow : VersionedRow
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

        /// <summary>Gets or sets the placement id.</summary>
        [Column("placement_id")]
        public string PlacementId { get; set; }

        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the point id.</summary>
        [Column("point_id")]
        public string PointId { get; set; }

        /// <summary>Gets or sets the target angle deg.</summary>
        [Column("target_angle_deg")]
        public double TargetAngleDeg { get; set; }

        /// <summary>Gets or sets the tolerance deg.</summary>
        [Column("tolerance_deg")]
        public double ToleranceDeg { get; set; }
    }
}
