namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_item_actions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_item_actions")]
    public sealed class PuzzleItemActionRow : VersionedRow
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

        /// <summary>Gets or sets the action number.</summary>
        [Column("action_number")]
        public long ActionNumber { get; set; }

        /// <summary>Gets or sets the kind.</summary>
        [Column("kind")]
        public string Kind { get; set; }

        /// <summary>Gets or sets the placement id.</summary>
        [Column("placement_id")]
        public string PlacementId { get; set; }

        /// <summary>Gets or sets the operation.</summary>
        [Column("operation")]
        public string Operation { get; set; }
    }
}
