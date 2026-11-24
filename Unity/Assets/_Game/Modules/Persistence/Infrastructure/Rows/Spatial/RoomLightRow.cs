namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the room_lights relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("room_lights")]
    public sealed class RoomLightRow : VersionedRow
    {
        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the anchor id.</summary>
        [Column("anchor_id")]
        public string AnchorId { get; set; }

        /// <summary>Gets or sets the intensity.</summary>
        [Column("intensity")]
        public double Intensity { get; set; }

        /// <summary>Gets or sets the range m.</summary>
        [Column("range_m")]
        public double RangeM { get; set; }

        /// <summary>Gets or sets the red.</summary>
        [Column("red")]
        public double Red { get; set; }

        /// <summary>Gets or sets the green.</summary>
        [Column("green")]
        public double Green { get; set; }

        /// <summary>Gets or sets the blue.</summary>
        [Column("blue")]
        public double Blue { get; set; }
    }
}
