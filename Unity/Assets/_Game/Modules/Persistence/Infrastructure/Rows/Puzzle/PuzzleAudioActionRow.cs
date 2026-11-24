namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzle_audio_actions relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzle_audio_actions")]
    public sealed class PuzzleAudioActionRow : VersionedRow
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

        /// <summary>Gets or sets the audio asset id.</summary>
        [Column("audio_asset_id")]
        public string AudioAssetId { get; set; }

        /// <summary>Gets or sets the volume.</summary>
        [Column("volume")]
        public double Volume { get; set; }

        /// <summary>Gets or sets the source placement id.</summary>
        [Column("source_placement_id")]
        public string SourcePlacementId { get; set; }
    }
}
