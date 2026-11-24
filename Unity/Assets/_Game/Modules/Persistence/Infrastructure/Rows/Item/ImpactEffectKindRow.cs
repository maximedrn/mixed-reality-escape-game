namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the impact_effect_kinds relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("impact_effect_kinds")]
    public sealed class ImpactEffectKindRow
    {
        /// <summary>Gets or sets the id.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }
    }
}
