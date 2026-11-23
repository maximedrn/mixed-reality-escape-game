namespace Project.Tests.EditMode
{
    using System;
    using NUnit.Framework;
    using Project.Core;
    using Project.GameFlow.Application;
    using Project.GameFlow.Domain;

    /// <summary>Verifies session initialization and the allowed state transitions.</summary>
    public sealed class SessionServiceTests
    {
        /// <summary>A new session starts ready and keeps its supplied identity.</summary>
        [Test]
        public void CreateStartsReady()
        {
            Guid id = Guid.NewGuid();
            Result<GameSession, SessionError> result = SessionService.Create(
                new SessionId(id)
            );

            Assert.That(result.TryGetValue(out GameSession session), Is.True);
            Assert.That(session.Id.Value, Is.EqualTo(id));
            Assert.That(session.State, Is.EqualTo(GameState.Ready));
        }

        /// <summary>A session requires a nonempty identity.</summary>
        [Test]
        public void CreateRejectsEmptyIdentity()
        {
            Result<GameSession, SessionError> result = SessionService.Create(
                new SessionId(Guid.Empty)
            );

            Assert.That(result.TryGetError(out SessionError error), Is.True);
            Assert.That(error, Is.EqualTo(SessionError.InvalidId));
        }

        /// <summary>Only an active session can finish, and finished sessions are immutable.</summary>
        /// <param name="outcome">The final session state.</param>
        [TestCase(GameState.Won)]
        [TestCase(GameState.Lost)]
        public void PlayingSessionCanFinish(GameState outcome)
        {
            GameSession ready = CreateReadySession();
            Result<GameSession, SessionError> start = SessionService.Transition(
                ready,
                GameState.Playing
            );
            Assert.That(start.TryGetValue(out GameSession playing), Is.True);

            Result<GameSession, SessionError> end = SessionService.Transition(
                playing,
                outcome
            );

            Assert.That(end.TryGetValue(out GameSession finished), Is.True);
            Assert.That(finished.Id.Value, Is.EqualTo(ready.Id.Value));
            Assert.That(finished.State, Is.EqualTo(outcome));
            Assert.That(playing.State, Is.EqualTo(GameState.Playing));
            Assert.That(ready.State, Is.EqualTo(GameState.Ready));
            Assert.That(
                SessionService
                    .Transition(finished, GameState.Playing)
                    .IsFailure,
                Is.True
            );
        }

        /// <summary>A ready session cannot skip the playing state.</summary>
        /// <param name="outcome">The attempted final session state.</param>
        [TestCase(GameState.Won)]
        [TestCase(GameState.Lost)]
        public void ReadySessionCannotFinish(GameState outcome)
        {
            Result<GameSession, SessionError> result =
                SessionService.Transition(CreateReadySession(), outcome);

            Assert.That(result.TryGetError(out SessionError error), Is.True);
            Assert.That(error, Is.EqualTo(SessionError.InvalidTransition));
        }

        /// <summary>A default session cannot be started.</summary>
        [Test]
        public void UninitializedSessionCannotStart()
        {
            Result<GameSession, SessionError> result =
                SessionService.Transition(
                    default(GameSession),
                    GameState.Playing
                );

            Assert.That(result.TryGetError(out SessionError error), Is.True);
            Assert.That(error, Is.EqualTo(SessionError.InvalidId));
        }

        /// <summary>Creates a valid session for transition tests.</summary>
        /// <returns>A new session in the ready state.</returns>
        private static GameSession CreateReadySession()
        {
            Result<GameSession, SessionError> result = SessionService.Create(
                new SessionId(Guid.NewGuid())
            );
            Assert.That(result.TryGetValue(out GameSession session), Is.True);
            return session;
        }
    }
}
