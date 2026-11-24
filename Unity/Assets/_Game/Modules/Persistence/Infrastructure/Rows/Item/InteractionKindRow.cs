namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the interaction_kinds relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("interaction_kinds")]
    public sealed class InteractionKindRow
    {
        /// <summary>Gets or sets the id.</summary>
        [PrimaryKey]
        [Column("id")]
        public string Id { get; set; }
    }
}
