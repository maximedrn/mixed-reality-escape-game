namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the room_anchors relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("room_anchors")]
    public sealed class RoomAnchorRow : VersionedRow
    {
        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the position x m.</summary>
        [Column("position_x_m")]
        public double PositionXM { get; set; }

        /// <summary>Gets or sets the position y m.</summary>
        [Column("position_y_m")]
        public double PositionYM { get; set; }

        /// <summary>Gets or sets the position z m.</summary>
        [Column("position_z_m")]
        public double PositionZM { get; set; }

        /// <summary>Gets or sets the rotation x.</summary>
        [Column("rotation_x")]
        public double RotationX { get; set; }

        /// <summary>Gets or sets the rotation y.</summary>
        [Column("rotation_y")]
        public double RotationY { get; set; }

        /// <summary>Gets or sets the rotation z.</summary>
        [Column("rotation_z")]
        public double RotationZ { get; set; }

        /// <summary>Gets or sets the rotation w.</summary>
        [Column("rotation_w")]
        public double RotationW { get; set; }
    }
}
