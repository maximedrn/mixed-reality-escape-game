namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the room_calibration_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("room_calibration_settings")]
    public sealed class RoomCalibrationSettingRow : VersionedRow
    {
        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the min fixed markers.</summary>
        [Column("min_fixed_markers")]
        public long MinFixedMarkers { get; set; }

        /// <summary>Gets or sets the position tolerance m.</summary>
        [Column("position_tolerance_m")]
        public double PositionToleranceM { get; set; }

        /// <summary>Gets or sets the rotation tolerance deg.</summary>
        [Column("rotation_tolerance_deg")]
        public double RotationToleranceDeg { get; set; }

        /// <summary>Gets or sets the detection timeout ms.</summary>
        [Column("detection_timeout_ms")]
        public long DetectionTimeoutMs { get; set; }
    }
}
