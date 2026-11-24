namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the scenario_items relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("scenario_items")]
    public sealed class ScenarioItemRow : VersionedRow
    {
        /// <summary>Gets or sets the scenario id.</summary>
        [Column("scenario_id")]
        public string ScenarioId { get; set; }

        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the item id.</summary>
        [Column("item_id")]
        public string ItemId { get; set; }

        /// <summary>Gets or sets the anchor id.</summary>
        [Column("anchor_id")]
        public string AnchorId { get; set; }
    }
}
