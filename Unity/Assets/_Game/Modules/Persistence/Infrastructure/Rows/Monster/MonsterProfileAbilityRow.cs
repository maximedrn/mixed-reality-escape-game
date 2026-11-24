namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_profile_abilities relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_profile_abilities")]
    public sealed class MonsterProfileAbilityRow : VersionedRow
    {
        /// <summary>Gets or sets the monster id.</summary>
        [Column("monster_id")]
        public string MonsterId { get; set; }

        /// <summary>Gets or sets the difficulty id.</summary>
        [Column("difficulty_id")]
        public string DifficultyId { get; set; }

        /// <summary>Gets or sets the ability id.</summary>
        [Column("ability_id")]
        public string AbilityId { get; set; }
    }
}
