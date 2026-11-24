namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the session_item_stats relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("session_item_stats")]
    public sealed class SessionItemStatsRow : RulesetStatisticRow
    {
        /// <summary>Gets or sets the placement id.</summary>
        [Column("placement_id")]
        public string PlacementId { get; set; }

        /// <summary>Gets or sets the grabs.</summary>
        [Column("grabs")]
        public long Grabs { get; set; }

        /// <summary>Gets or sets the throws.</summary>
        [Column("throws")]
        public long Throws { get; set; }

        /// <summary>Gets or sets the activations.</summary>
        [Column("activations")]
        public long Activations { get; set; }

        /// <summary>Gets or sets the breaks.</summary>
        [Column("breaks")]
        public long Breaks { get; set; }
    }
}
