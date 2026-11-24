namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the rooms relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("rooms")]
    public sealed class RoomRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the scene asset id.</summary>
        [Column("scene_asset_id")]
        public string SceneAssetId { get; set; }

        /// <summary>Gets or sets the visible asset id.</summary>
        [Column("visible_asset_id")]
        public string VisibleAssetId { get; set; }

        /// <summary>Gets or sets the collision asset id.</summary>
        [Column("collision_asset_id")]
        public string CollisionAssetId { get; set; }

        /// <summary>Gets or sets the ambience audio asset id.</summary>
        [Column("ambience_audio_asset_id")]
        public string AmbienceAudioAssetId { get; set; }

        /// <summary>Gets or sets the ambience volume.</summary>
        [Column("ambience_volume")]
        public double? AmbienceVolume { get; set; }
    }
}
