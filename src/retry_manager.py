
import time
import random
from functools import wraps

from config import MAX_RETRIES


def retry(
    max_retries=MAX_RETRIES,
    base_delay=1,
    max_delay=10,
    retryable_exceptions=(Exception,)
):
    """
    Retry decorator with exponential backoff and jitter.

    max_retries:
        Number of retries after the first attempt.

    base_delay:
        Initial waiting time in seconds.

    max_delay:
        Maximum waiting time in seconds.

    retryable_exceptions:
        Exceptions that should trigger a retry.
    """

    if max_retries < 0:
        raise ValueError("max_retries cannot be negative.")

    if base_delay < 0 or max_delay < 0:
        raise ValueError("Delay values cannot be negative.")

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            attempt = 0

            while True:
                try:
                    print(
                        f"\nAttempt {attempt + 1} "
                        f"of {max_retries + 1}..."
                    )

                    result = func(*args, **kwargs)

                    print("Request successful!")
                    return result

                except retryable_exceptions as error:

                    if attempt >= max_retries:
                        print("Maximum retries reached.")
                        raise

                    delay = min(
                        base_delay * (2 ** attempt),
                        max_delay
                    )

                    # Add random jitter to avoid simultaneous retries
                    jitter = random.uniform(0, delay * 0.2)
                    wait_time = delay + jitter

                    print(f"Request failed: {error}")
                    print(
                        f"Retrying in {wait_time:.2f} seconds..."
                    )

                    time.sleep(wait_time)
                    attempt += 1

        return wrapper

    return decorator


# ---------------------------------------
# TEST FUNCTION
# ---------------------------------------

def main():

    print("=" * 40)
    print("THE RELAY - RETRY MANAGER TEST")
    print("=" * 40)

    # Simulate an API that fails twice
    # and succeeds on the third attempt.

    request_count = {"count": 0}

    @retry(
        max_retries=3,
        base_delay=1,
        max_delay=5
    )
    def simulated_api_request():

        request_count["count"] += 1

        print(
            f"Simulated API call: "
            f"{request_count['count']}"
        )

        if request_count["count"] < 3:
            raise ConnectionError(
                "Temporary API connection failure"
            )

        return {
            "status": "success",
            "message": "API response received successfully."
        }

    try:
        response = simulated_api_request()

        print("\nFinal API Response:")
        print(response)

        print(
            "\nTotal Attempts:",
            request_count["count"]
        )

    except Exception as error:
        print("\nAPI request failed:", error)


if __name__ == "__main__":
    main()
