namespace Project.Persistence
{
    using SQLite;

    /// <summary>Maps a row from the physics_profiles relation.</summary>
    [UnityEngine.Scripting.Preserve]
    [Table("physics_profiles")]
    public sealed class PhysicsProfileRow : VersionedRow
    {
        /// <summary>Gets or sets the id.</summary>
        [Column("id")]
        public string Id { get; set; }

        /// <summary>Gets or sets the min impact speed mps.</summary>
        [Column("min_impact_speed_mps")]
        public double MinImpactSpeedMps { get; set; }

        /// <summary>Gets or sets the noise per mps.</summary>
        [Column("noise_per_mps")]
        public double NoisePerMps { get; set; }
    }
}
