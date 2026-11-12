
import time
from src.rate_limiter import TokenBucket


def run_test(test_name, requests_per_minute):

    print("\n" + "=" * 50)
    print("TEST:", test_name)
    print("Rate Limit:", requests_per_minute, "requests/minute")
    print("=" * 50)

    limiter = TokenBucket(
        capacity=2,
        refill_rate=requests_per_minute / 60
    )

    total_requests = 4
    successful = 0
    start_time = time.perf_counter()

    for request_id in range(1, total_requests + 1):

        request_start = time.perf_counter()

        print(f"\nRequest {request_id}: Waiting for token...")

        acquired = limiter.acquire()

        request_time = time.perf_counter() - request_start

        if acquired:
            successful += 1
            print("Status: SUCCESS")
            print("Wait Time:", round(request_time, 2), "seconds")

    total_time = time.perf_counter() - start_time

    print("\n--- Test Summary ---")
    print("Total Requests:", total_requests)
    print("Successful:", successful)
    print("Failed:", total_requests - successful)
    print("Total Time:", round(total_time, 2), "seconds")

    return {
        "test": test_name,
        "limit": requests_per_minute,
        "successful": successful,
        "total_time": round(total_time, 2)
    }


def main():

    print("THE RELAY - HALVED RATE LIMIT SIMULATION")

    original = run_test(
        test_name="Original Limit",
        requests_per_minute=10
    )

    reduced = run_test(
        test_name="Halved Limit",
        requests_per_minute=5
    )

    print("\n" + "=" * 50)
    print("FINAL COMPARISON")
    print("=" * 50)

    print(original)
    print(reduced)


if __name__ == "__main__":
    main()
