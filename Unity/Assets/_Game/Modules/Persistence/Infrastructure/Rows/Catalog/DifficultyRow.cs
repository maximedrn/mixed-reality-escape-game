namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the difficulties relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("difficulties")]
    public sealed class DifficultyRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the display order.</summary>
        [Column("display_order")]
        public long DisplayOrder { get; set; }

        /// <summary>Gets or sets the allows monster.</summary>
        [Column("allows_monster")]
        public long AllowsMonster { get; set; }
    }
}
