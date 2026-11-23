namespace Project.GameFlow.Application
{
    using System;
    using Project.Core;
    using Project.GameFlow.Domain;

    /// <summary>Creates sessions and advances them through the game lifecycle.</summary>
    public static class SessionService
    {
        /// <summary>Creates a session ready to start.</summary>
        /// <param name="id">The stable identifier supplied by the caller.</param>
        /// <returns>The new session or an error for an empty identifier.</returns>
        public static Result<GameSession, SessionError> Create(SessionId id)
        {
            if (id.Value == Guid.Empty)
            {
                return Result<GameSession, SessionError>.Fail(
                    SessionError.InvalidId
                );
            }

            return Result<GameSession, SessionError>.Ok(
                new GameSession(id, GameState.Ready)
            );
        }

        /// <summary>Tries to advance a session to the requested state.</summary>
        /// <param name="session">The current, initialized session.</param>
        /// <param name="target">The requested next state.</param>
        /// <returns>The updated session or the reason the transition failed.</returns>
        public static Result<GameSession, SessionError> Transition(
            GameSession session,
            GameState target
        )
        {
            if (session.Id.Value == Guid.Empty)
            {
                return Result<GameSession, SessionError>.Fail(
                    SessionError.InvalidId
                );
            }

            bool allowed = (session.State, target) switch
            {
                (GameState.Ready, GameState.Playing) => true,
                (GameState.Playing, GameState.Won or GameState.Lost) => true,
                _ => false,
            };
            if (!allowed)
            {
                return Result<GameSession, SessionError>.Fail(
                    SessionError.InvalidTransition
                );
            }

            return Result<GameSession, SessionError>.Ok(
                new GameSession(session.Id, target)
            );
        }
    }
}
