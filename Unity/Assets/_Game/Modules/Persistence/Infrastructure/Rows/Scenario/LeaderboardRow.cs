namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the leaderboards relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("leaderboards")]
    public sealed class LeaderboardRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the ranked layout id.</summary>
        [Column("ranked_layout_id")]
        public string RankedLayoutId { get; set; }

        /// <summary>Gets or sets the display limit.</summary>
        [Column("display_limit")]
        public long DisplayLimit { get; set; }
    }
}
