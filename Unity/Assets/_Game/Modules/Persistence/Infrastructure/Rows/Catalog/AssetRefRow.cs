namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the asset_refs relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("asset_refs")]
    public sealed class AssetRefRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the unity key.</summary>
        [Column("unity_key")]
        public string UnityKey { get; set; }

        /// <summary>Gets or sets the kind.</summary>
        [Column("kind")]
        public string Kind { get; set; }
    }
}
