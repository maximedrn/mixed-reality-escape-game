namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the item_rotate_settings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("item_rotate_settings")]
    public sealed class ItemRotateSettingRow : VersionedRow
    {
        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the point id.</summary>
        [Column("point_id")]
        public string PointId { get; set; }

        /// <summary>Gets or sets the kind id.</summary>
        [Column("kind_id")]
        public string KindId { get; set; }

        /// <summary>Gets or sets the axis x.</summary>
        [Column("axis_x")]
        public double AxisX { get; set; }

        /// <summary>Gets or sets the axis y.</summary>
        [Column("axis_y")]
        public double AxisY { get; set; }

        /// <summary>Gets or sets the axis z.</summary>
        [Column("axis_z")]
        public double AxisZ { get; set; }

        /// <summary>Gets or sets the min angle deg.</summary>
        [Column("min_angle_deg")]
        public double MinAngleDeg { get; set; }

        /// <summary>Gets or sets the max angle deg.</summary>
        [Column("max_angle_deg")]
        public double MaxAngleDeg { get; set; }
    }
}
