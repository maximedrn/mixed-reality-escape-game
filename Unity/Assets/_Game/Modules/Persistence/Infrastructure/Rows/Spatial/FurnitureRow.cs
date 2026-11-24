namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the furniture relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("furniture")]
    public sealed class FurnitureRow : VersionedRow
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

        /// <summary>Gets or sets the width m.</summary>
        [Column("width_m")]
        public double WidthM { get; set; }

        /// <summary>Gets or sets the height m.</summary>
        [Column("height_m")]
        public double HeightM { get; set; }

        /// <summary>Gets or sets the depth m.</summary>
        [Column("depth_m")]
        public double DepthM { get; set; }

        /// <summary>Gets or sets the visible prefab asset id.</summary>
        [Column("visible_prefab_asset_id")]
        public string VisiblePrefabAssetId { get; set; }

        /// <summary>Gets or sets the collision prefab asset id.</summary>
        [Column("collision_prefab_asset_id")]
        public string CollisionPrefabAssetId { get; set; }

        /// <summary>Gets or sets the required for calibration.</summary>
        [Column("required_for_calibration")]
        public long RequiredForCalibration { get; set; }
    }
}
