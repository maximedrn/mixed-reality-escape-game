namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a local player to the players table.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("players")]
    public sealed class PlayerRow
    {
        /// <summary>Gets or sets the stable player identifier.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the name displayed in the game.</summary>
        [Column("display_name")]
        public string DisplayName { get; set; }

        /// <summary>Gets or sets the creation timestamp in Unix milliseconds.</summary>
        [Column("created_at_utc_ms")]
        public long CreatedAtUtcMs { get; set; }
    }
}
