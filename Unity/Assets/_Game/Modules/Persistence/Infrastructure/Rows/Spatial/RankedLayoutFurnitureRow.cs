namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ranked_layout_furniture relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ranked_layout_furniture")]
    public sealed class RankedLayoutFurnitureRow : VersionedRow
    {
        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the layout id.</summary>
        [Column("layout_id")]
        public string LayoutId { get; set; }

        /// <summary>Gets or sets the furniture id.</summary>
        [Column("furniture_id")]
        public string FurnitureId { get; set; }

        /// <summary>Gets or sets the expected anchor id.</summary>
        [Column("expected_anchor_id")]
        public string ExpectedAnchorId { get; set; }
    }
}
