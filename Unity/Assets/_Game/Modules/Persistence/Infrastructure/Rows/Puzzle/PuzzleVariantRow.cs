namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_variants relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_variants")]
    public sealed class PuzzleVariantRow : VersionedRow
    {
        /// <summary>Gets or sets the scenario id.</summary>
        [Column("scenario_id")]
        public string ScenarioId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the puzzle id.</summary>
        [Column("puzzle_id")]
        public string PuzzleId { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }
    }
}
