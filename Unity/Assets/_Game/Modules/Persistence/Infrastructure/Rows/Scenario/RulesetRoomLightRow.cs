namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the ruleset_room_lights relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("ruleset_room_lights")]
    public sealed class RulesetRoomLightRow : VersionedRow
    {
        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the light id.</summary>
        [Column("light_id")]
        public string LightId { get; set; }
    }
}
