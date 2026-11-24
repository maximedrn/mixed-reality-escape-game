namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_audio_bindings relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_audio_bindings")]
    public sealed class MonsterAudioBindingRow : VersionedRow
    {
        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the event.</summary>
        [Column("event")]
        public string Event { get; set; }

        /// <summary>Gets or sets the slot.</summary>
        [Column("slot")]
        public long Slot { get; set; }

        /// <summary>Gets or sets the audio asset id.</summary>
        [Column("audio_asset_id")]
        public string AudioAssetId { get; set; }

        /// <summary>Gets or sets the volume.</summary>
        [Column("volume")]
        public double Volume { get; set; }
    }
}
