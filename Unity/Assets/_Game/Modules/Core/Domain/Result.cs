namespace Project.Core
{
    /// <summary>
    /// Represents the outcome of an operation without using exceptions for expected errors.
    /// An uninitialized default result is neither successful nor failed.
    /// </summary>
    /// <typeparam name="TValue">The successful value type.</typeparam>
    /// <typeparam name="TError">The expected error type.</typeparam>
    public readonly struct Result<TValue, TError>
    {
        private readonly TValue _value;
        private readonly TError _error;
        private readonly bool _isSuccess;

        /// <summary>
        /// Initializes a new instance of the <see cref="Result{TValue, TError}"/> struct.
        /// </summary>
        /// <param name="value">The successful value, if any.</param>
        /// <param name="error">The error value, if any.</param>
        /// <param name="isSuccess">Whether the result represents success.</param>
        private Result(TValue value, TError error, bool isSuccess)
        {
            this._value = value;
            this._error = error;
            this._isSuccess = isSuccess;
            this.IsInitialized = true;
        }

        /// <summary>Gets a value indicating whether a factory created the result.</summary>
        public bool IsInitialized { get; }

        /// <summary>Gets a value indicating whether the operation succeeded.</summary>
        public bool IsSuccess => this.IsInitialized && this._isSuccess;

        /// <summary>Gets a value indicating whether the operation returned an error.</summary>
        public bool IsFailure => this.IsInitialized && !this._isSuccess;

        /// <summary>Creates a successful result.</summary>
        /// <param name="value">The successful value.</param>
        /// <returns>A successful outcome.</returns>
        public static Result<TValue, TError> Ok(TValue value)
        {
            return new Result<TValue, TError>(value, default(TError), true);
        }

        /// <summary>Creates a failed result with a typed error.</summary>
        /// <param name="error">The expected error.</param>
        /// <returns>A failed outcome.</returns>
        public static Result<TValue, TError> Fail(TError error)
        {
            return new Result<TValue, TError>(default(TValue), error, false);
        }

        /// <summary>Tries to retrieve the successful value.</summary>
        /// <param name="value">The value, or its default when unsuccessful.</param>
        /// <returns>True only when the result is successful.</returns>
        public bool TryGetValue(out TValue value)
        {
            value = this._value;
            return this.IsSuccess;
        }

        /// <summary>Tries to retrieve the expected error.</summary>
        /// <param name="error">The error, or its default when not failed.</param>
        /// <returns>True only when the result represents a failure.</returns>
        public bool TryGetError(out TError error)
        {
            error = this._error;
            return this.IsFailure;
        }
    }
}
