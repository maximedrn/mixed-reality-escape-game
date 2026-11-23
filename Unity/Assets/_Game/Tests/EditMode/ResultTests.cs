namespace Project.Tests.EditMode
{
    using NUnit.Framework;
    using Project.Core;

    /// <summary>Verifies the behavior of typed operation outcomes.</summary>
    public sealed class ResultTests
    {
        /// <summary>A successful outcome exposes its value and not an error.</summary>
        [Test]
        public void OkReturnsExpectedValue()
        {
            const int ExpectedValue = 42;
            Result<int, SampleError> result = Result<int, SampleError>.Ok(
                ExpectedValue
            );

            Assert.That(result.IsInitialized, Is.True);
            Assert.That(result.IsSuccess, Is.True);
            Assert.That(result.IsFailure, Is.False);
            Assert.That(result.TryGetValue(out int value), Is.True);
            Assert.That(value, Is.EqualTo(ExpectedValue));
            Assert.That(result.TryGetError(out _), Is.False);
        }

        /// <summary>A failure exposes its typed error and not a value.</summary>
        [Test]
        public void FailReturnsExpectedError()
        {
            Result<int, SampleError> result = Result<int, SampleError>.Fail(
                SampleError.Unavailable
            );

            Assert.That(result.IsInitialized, Is.True);
            Assert.That(result.IsSuccess, Is.False);
            Assert.That(result.IsFailure, Is.True);
            Assert.That(result.TryGetValue(out _), Is.False);
            Assert.That(result.TryGetError(out SampleError error), Is.True);
            Assert.That(error, Is.EqualTo(SampleError.Unavailable));
        }

        /// <summary>A default-initialized value must not claim either outcome.</summary>
        [Test]
        public void DefaultResultIsNotAnOutcome()
        {
            Result<Unit, SampleError> result = default(Result<
                Unit,
                SampleError
            >);

            Assert.That(result.IsInitialized, Is.False);
            Assert.That(result.IsSuccess, Is.False);
            Assert.That(result.IsFailure, Is.False);
            Assert.That(result.TryGetValue(out _), Is.False);
            Assert.That(result.TryGetError(out _), Is.False);
        }

        /// <summary>Errors used only by the result contract tests.</summary>
        private enum SampleError
        {
            /// <summary>Represents an unavailable value.</summary>
            Unavailable,
        }
    }
}
