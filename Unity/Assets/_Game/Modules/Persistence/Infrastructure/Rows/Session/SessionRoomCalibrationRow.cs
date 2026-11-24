namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the session_room_calibrations relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("session_room_calibrations")]
    public sealed class SessionRoomCalibrationRow : SessionStatisticRow
    {
        /// <summary>Gets or sets the duration ms.</summary>
        [Column("duration_ms")]
        public long DurationMs { get; set; }

        /// <summary>Gets or sets the fixed markers seen.</summary>
        [Column("fixed_markers_seen")]
        public long FixedMarkersSeen { get; set; }

        /// <summary>Gets or sets the position error m.</summary>
        [Column("position_error_m")]
        public double? PositionErrorM { get; set; }

        /// <summary>Gets or sets the rotation error deg.</summary>
        [Column("rotation_error_deg")]
        public double? RotationErrorDeg { get; set; }
    }
}
