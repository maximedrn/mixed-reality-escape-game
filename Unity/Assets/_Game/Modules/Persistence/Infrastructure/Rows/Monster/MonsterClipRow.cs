namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_clips relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_clips")]
    public sealed class MonsterClipRow : VersionedRow
    {
        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the clip name.</summary>
        [Column("clip_name")]
        public string ClipName { get; set; }

        /// <summary>Gets or sets the clip asset id.</summary>
        [Column("clip_asset_id")]
        public string ClipAssetId { get; set; }
    }
}
