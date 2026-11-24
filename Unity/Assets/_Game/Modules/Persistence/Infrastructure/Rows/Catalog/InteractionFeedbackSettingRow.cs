namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the interaction_feedback_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("interaction_feedback_settings")]
    public sealed class InteractionFeedbackSettingRow : VersionedRow
    {
        /// <summary>Gets or sets the interaction profile id.</summary>
        [Column("interaction_profile_id")]
        public string InteractionProfileId { get; set; }

        /// <summary>Gets or sets the target kind.</summary>
        [Column("target_kind")]
        public string TargetKind { get; set; }

        /// <summary>Gets or sets the red.</summary>
        [Column("red")]
        public double Red { get; set; }

        /// <summary>Gets or sets the green.</summary>
        [Column("green")]
        public double Green { get; set; }

        /// <summary>Gets or sets the blue.</summary>
        [Column("blue")]
        public double Blue { get; set; }

        /// <summary>Gets or sets the intensity.</summary>
        [Column("intensity")]
        public double Intensity { get; set; }
    }
}
