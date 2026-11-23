namespace Project.Core
{
    /// <summary>Represents successful operations without a return payload.</summary>
    public readonly struct Unit
    {
        /// <summary>Gets the single meaningful unit value.</summary>
        public static Unit Value => default(Unit);
    }
}
