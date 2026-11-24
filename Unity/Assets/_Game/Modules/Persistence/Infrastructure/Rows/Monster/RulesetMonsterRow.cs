namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ruleset_monsters relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ruleset_monsters")]
    public sealed class RulesetMonsterRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the difficulty id.</summary>
        [Column("difficulty_id")]
        public string DifficultyId { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the spawn anchor id.</summary>
        [Column("spawn_anchor_id")]
        public string SpawnAnchorId { get; set; }
    }
}
