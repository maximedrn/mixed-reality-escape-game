namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the interaction_profiles relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("interaction_profiles")]
    public sealed class InteractionProfileRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the grab distance m.</summary>
        [Column("grab_distance_m")]
        public double GrabDistanceM { get; set; }

        /// <summary>Gets or sets the pinch distance m.</summary>
        [Column("pinch_distance_m")]
        public double PinchDistanceM { get; set; }

        /// <summary>Gets or sets the press distance m.</summary>
        [Column("press_distance_m")]
        public double PressDistanceM { get; set; }

        /// <summary>Gets or sets the open hand confidence.</summary>
        [Column("open_hand_confidence")]
        public double OpenHandConfidence { get; set; }

        /// <summary>Gets or sets the closed hand confidence.</summary>
        [Column("closed_hand_confidence")]
        public double ClosedHandConfidence { get; set; }

        /// <summary>Gets or sets the pinch confidence.</summary>
        [Column("pinch_confidence")]
        public double PinchConfidence { get; set; }

        /// <summary>Gets or sets the point confidence.</summary>
        [Column("point_confidence")]
        public double PointConfidence { get; set; }

        /// <summary>Gets or sets the gesture stabilization ms.</summary>
        [Column("gesture_stabilization_ms")]
        public long GestureStabilizationMs { get; set; }

        /// <summary>Gets or sets the max charge ms.</summary>
        [Column("max_charge_ms")]
        public long MaxChargeMs { get; set; }

        /// <summary>Gets or sets the maximum assisted launch speed in metres per second.</summary>
        [Column("max_throw_speed_mps")]
        public double MaxThrowSpeedMps { get; set; }

        /// <summary>Gets or sets the aim smoothing ms.</summary>
        [Column("aim_smoothing_ms")]
        public long AimSmoothingMs { get; set; }
    }
}
