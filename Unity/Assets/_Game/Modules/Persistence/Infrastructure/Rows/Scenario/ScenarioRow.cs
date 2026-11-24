namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the scenarios relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("scenarios")]
    public sealed class ScenarioRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the room id.</summary>
        [Column("room_id")]
        public string RoomId { get; set; }

        /// <summary>Gets or sets the label.</summary>
        [Column("label")]
        public string Label { get; set; }

        /// <summary>Gets or sets the player spawn anchor id.</summary>
        [Column("player_spawn_anchor_id")]
        public string PlayerSpawnAnchorId { get; set; }

        /// <summary>Gets or sets the exit anchor id.</summary>
        [Column("exit_anchor_id")]
        public string ExitAnchorId { get; set; }

        /// <summary>Gets or sets the interaction profile id.</summary>
        [Column("interaction_profile_id")]
        public string InteractionProfileId { get; set; }

        /// <summary>Gets or sets the physics profile id.</summary>
        [Column("physics_profile_id")]
        public string PhysicsProfileId { get; set; }
    }
}
