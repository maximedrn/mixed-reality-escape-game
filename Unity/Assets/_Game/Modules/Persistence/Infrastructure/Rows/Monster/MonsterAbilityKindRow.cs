namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the monster_ability_kinds relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("monster_ability_kinds")]
    public sealed class MonsterAbilityKindRow
    {
        /// <summary>Gets or sets the id.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }
    }
}
