namespace Project.Core
{
    /// <summary>Represents the overall progression of a game session.</summary>
    public enum GameState
    {
        /// <summary>The session is ready to start.</summary>
        Ready,

        /// <summary>The player is actively playing.</summary>
        Playing,

        /// <summary>The player has completed the session.</summary>
        Won,

        /// <summary>The player has lost the session.</summary>
        Lost,
    }
}
