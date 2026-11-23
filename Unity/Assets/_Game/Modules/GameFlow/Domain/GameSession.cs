namespace Project.GameFlow.Domain
{
    using Project.Core;

    /// <summary>Captures the identity and current state of a game session.</summary>
    public readonly struct GameSession
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="GameSession"/> struct.
        /// </summary>
        /// <param name="id">The identity that stays stable throughout the session.</param>
        /// <param name="state">The current state.</param>
        internal GameSession(SessionId id, GameState state)
        {
            this.Id = id;
            this.State = state;
        }

        /// <summary>Gets the permanent identity of the session.</summary>
        public SessionId Id { get; }

        /// <summary>Gets the state reached by the session.</summary>
        public GameState State { get; }
    }
}
