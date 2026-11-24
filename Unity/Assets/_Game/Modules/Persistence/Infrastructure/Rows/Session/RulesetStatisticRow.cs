namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps the ruleset identity of session statistics.</summary>
    public abstract class RulesetStatisticRow : SessionStatisticRow
    {
        /// <summary>Gets or sets the content version id.</summary>
        [Column("content_version_id")]
        public string ContentVersionId { get; set; }

        /// <summary>Gets or sets the ruleset id.</summary>
        [Column("ruleset_id")]
        public string RulesetId { get; set; }
    }
}
