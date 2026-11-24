namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the rulesets relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("rulesets")]
    public sealed class RulesetRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the scenario id.</summary>
        [Column("scenario_id")]
        public string ScenarioId { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the difficulty id.</summary>
        [Column("difficulty_id")]
        public string DifficultyId { get; set; }
    }
}
