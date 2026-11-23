namespace Project.Puzzles
{
    /// <summary>Represents the progression of a puzzle.</summary>
    public enum PuzzleState
    {
        /// <summary>The puzzle cannot be attempted yet.</summary>
        Locked,

        /// <summary>The puzzle can be attempted.</summary>
        Available,

        /// <summary>The puzzle has been completed.</summary>
        Solved,
    }
}
