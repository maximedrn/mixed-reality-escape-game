namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ruleset_items relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ruleset_items")]
    public sealed class RulesetItemRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the scenario id.</summary>
        [Column("scenario_id")]
        public string ScenarioId { get; set; }

        /// <summary>Gets or sets the placement id.</summary>
        [Column("placement_id")]
        public string PlacementId { get; set; }

        /// <summary>Gets or sets the spawn on start.</summary>
        [Column("spawn_on_start")]
        public long SpawnOnStart { get; set; }
    }
}
