namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the room_decorations relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("room_decorations")]
    public sealed class RoomDecorationRow : VersionedRow
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

        /// <summary>Gets or sets the prefab asset id.</summary>
        [Column("prefab_asset_id")]
        public string PrefabAssetId { get; set; }
    }
}
