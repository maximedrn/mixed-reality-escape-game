namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the qr_markers relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("qr_markers")]
    public sealed class QrMarkerRow : VersionedRow
    {
        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the payload.</summary>
        [Column("payload")]
        public string Payload { get; set; }

        /// <summary>Gets or sets the furniture id.</summary>
        [Column("furniture_id")]
        public string FurnitureId { get; set; }

        /// <summary>Gets or sets the edge size m.</summary>
        [Column("edge_size_m")]
        public double EdgeSizeM { get; set; }

        /// <summary>Gets or sets the local position x m.</summary>
        [Column("local_position_x_m")]
        public double LocalPositionXM { get; set; }

        /// <summary>Gets or sets the local position y m.</summary>
        [Column("local_position_y_m")]
        public double LocalPositionYM { get; set; }

        /// <summary>Gets or sets the local position z m.</summary>
        [Column("local_position_z_m")]
        public double LocalPositionZM { get; set; }

        /// <summary>Gets or sets the local rotation x.</summary>
        [Column("local_rotation_x")]
        public double LocalRotationX { get; set; }

        /// <summary>Gets or sets the local rotation y.</summary>
        [Column("local_rotation_y")]
        public double LocalRotationY { get; set; }

        /// <summary>Gets or sets the local rotation z.</summary>
        [Column("local_rotation_z")]
        public double LocalRotationZ { get; set; }

        /// <summary>Gets or sets the local rotation w.</summary>
        [Column("local_rotation_w")]
        public double LocalRotationW { get; set; }
    }
}
