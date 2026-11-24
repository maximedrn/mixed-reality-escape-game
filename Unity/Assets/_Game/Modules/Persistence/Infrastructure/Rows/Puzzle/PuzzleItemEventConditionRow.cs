namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_item_event_conditions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_item_event_conditions")]
    public sealed class PuzzleItemEventConditionRow : VersionedRow
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

        /// <summary>Gets or sets the event.</summary>
        [Column("event")]
        public string Event { get; set; }

        /// <summary>Gets or sets the required count.</summary>
        [Column("required_count")]
        public long RequiredCount { get; set; }
    }
}
