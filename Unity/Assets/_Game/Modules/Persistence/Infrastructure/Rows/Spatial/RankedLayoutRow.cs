namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ranked_layouts relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ranked_layouts")]
    public sealed class RankedLayoutRow : VersionedRow
    {
        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the position tolerance m.</summary>
        [Column("position_tolerance_m")]
        public double PositionToleranceM { get; set; }

        /// <summary>Gets or sets the rotation tolerance deg.</summary>
        [Column("rotation_tolerance_deg")]
        public double RotationToleranceDeg { get; set; }
    }
}
