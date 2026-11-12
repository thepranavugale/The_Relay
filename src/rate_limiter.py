
import time
import threading


class TokenBucket:

    def __init__(self, capacity=10, refill_rate=10):

        if capacity <= 0:
            raise ValueError("Capacity must be positive.")

        if refill_rate <= 0:
            raise ValueError("Refill rate must be positive.")

        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)

        self.tokens = float(capacity)

        self.last_refill_time = time.monotonic()

        self.lock = threading.Lock()

    # -----------------------------------------
    # REFILL TOKENS
    # -----------------------------------------

    def _refill(self):

        current_time = time.monotonic()

        elapsed_time = (
            current_time - self.last_refill_time
        )

        new_tokens = elapsed_time * self.refill_rate

        self.tokens = min(
            self.capacity,
            self.tokens + new_tokens
        )

        self.last_refill_time = current_time

    # -----------------------------------------
    # CHECK AVAILABLE TOKENS
    # -----------------------------------------

    def available_tokens(self):

        with self.lock:

            self._refill()

            return self.tokens

    # -----------------------------------------
    # ACQUIRE TOKEN
    # -----------------------------------------

    def acquire(self, tokens=1, timeout=None):

        if tokens <= 0:
            raise ValueError("Requested tokens must be positive.")

        if tokens > self.capacity:
            raise ValueError(
                "Requested tokens exceed bucket capacity."
            )

        start_time = time.monotonic()

        while True:

            with self.lock:

                self._refill()

                if self.tokens >= tokens:

                    self.tokens -= tokens

                    return True

                missing_tokens = tokens - self.tokens

                wait_time = (
                    missing_tokens / self.refill_rate
                )

            if timeout is not None:

                elapsed = time.monotonic() - start_time

                remaining = timeout - elapsed

                if remaining <= 0 or wait_time > remaining:

                    return False

            time.sleep(wait_time)

    # -----------------------------------------
    # RESET BUCKET
    # -----------------------------------------

    def reset(self):

        with self.lock:

            self.tokens = self.capacity

            self.last_refill_time = time.monotonic()


# -----------------------------------------
# TEST TOKEN BUCKET
# -----------------------------------------

def main():

    print("================================")
    print("THE RELAY - RATE LIMITER")
    print("================================")

    limiter = TokenBucket(
        capacity=3,
        refill_rate=1
    )

    print("\nInitial Tokens:")

    print(limiter.available_tokens())

    print("\nRequest 1:")

    print("Acquired:", limiter.acquire())

    print("Remaining:", round(limiter.available_tokens(), 2))

    print("\nRequest 2:")

    print("Acquired:", limiter.acquire())

    print("Remaining:", round(limiter.available_tokens(), 2))

    print("\nRequest 3:")

    print("Acquired:", limiter.acquire())

    print("Remaining:", round(limiter.available_tokens(), 2))

    print("\nRequest 4:")

    print("Waiting for token...")

    result = limiter.acquire(timeout=3)

    print("Acquired:", result)

    print("Remaining:", round(limiter.available_tokens(), 2))

    print("\nRate Limiter Test Completed!")


if __name__ == "__main__":

    main()
