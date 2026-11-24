namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the puzzles relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("puzzles")]
    public sealed class PuzzleRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the title.</summary>
        [Column("title")]
        public string Title { get; set; }

        /// <summary>Gets or sets the technical difficulty.</summary>
        [Column("technical_difficulty")]
        public string TechnicalDifficulty { get; set; }
    }
}
