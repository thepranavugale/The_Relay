
# import time
# import csv
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor, as_completed

# from simulator.standin_model import StandInModel


# def run_single_request(model, request_id, scenario):
#     """Execute one simulated request and record its result."""

#     start_time = time.perf_counter()

#     try:
#         response = model.generate(
#             f"{scenario} research question {request_id}"
#         )
#         status = "SUCCESS"

#     except Exception as error:
#         response = str(error)
#         status = "FAILED"

#     end_time = time.perf_counter()

#     return {
#         "request_id": request_id,
#         "scenario": scenario,
#         "status": status,
#         "response_time": round(end_time - start_time, 4),
#         "response": response
#     }


# def run_scenario(scenario, total_requests, max_workers, response_delay=1):
#     """Run one load-test scenario."""

#     print("\n" + "=" * 60)
#     print(f"SCENARIO: {scenario}")
#     print("=" * 60)

#     model = StandInModel(
#         model_name="TheRelay-StandIn",
#         response_delay=response_delay,
#         failure_rate=0.0
#     )

#     results = []
#     overall_start = time.perf_counter()

#     print("Total Requests:", total_requests)
#     print("Concurrent Workers:", max_workers)
#     print("Response Delay:", response_delay, "seconds")
#     print("\nRunning...\n")

#     with ThreadPoolExecutor(max_workers=max_workers) as executor:

#         futures = [
#             executor.submit(
#                 run_single_request,
#                 model,
#                 request_id,
#                 scenario
#             )
#             for request_id in range(1, total_requests + 1)
#         ]

#         for future in as_completed(futures):
#             result = future.result()
#             results.append(result)

#             print(
#                 f"Request {result['request_id']}: "
#                 f"{result['status']} | "
#                 f"Time: {result['response_time']} seconds"
#             )

#     total_time = time.perf_counter() - overall_start

#     successful = sum(
#         result["status"] == "SUCCESS"
#         for result in results
#     )

#     failed = total_requests - successful

#     response_times = sorted(
#         result["response_time"] for result in results
#     )

#     average_time = sum(response_times) / len(response_times)

#     def percentile(values, percentile_value):
#         index = round((len(values) - 1) * percentile_value / 100)
#         return values[index]

#     print("\n--- Scenario Results ---")
#     print("Successful:", successful)
#     print("Failed:", failed)
#     print("Average Latency:", round(average_time, 4), "seconds")
#     print("Median Latency:", round(percentile(response_times, 50), 4))
#     print("P95 Latency:", round(percentile(response_times, 95), 4))
#     print("P99 Latency:", round(percentile(response_times, 99), 4))
#     print("Total Execution Time:", round(total_time, 4), "seconds")

#     for result in results:
#         result["total_execution_time"] = round(total_time, 4)

#     return results


# def run_all_load_tests():

#     all_results = []

#     # Scenario 1: Steady Load
#     steady_results = run_scenario(
#         scenario="steady_load",
#         total_requests=10,
#         max_workers=2,
#         response_delay=1
#     )
#     all_results.extend(steady_results)

#     # Scenario 2: Burst Load
#     burst_results = run_scenario(
#         scenario="burst_load",
#         total_requests=15,
#         max_workers=15,
#         response_delay=1
#     )
#     all_results.extend(burst_results)

#     # Scenario 3: Sustained Overload
#     overload_results = run_scenario(
#         scenario="sustained_overload",
#         total_requests=20,
#         max_workers=5,
#         response_delay=2
#     )
#     all_results.extend(overload_results)

#     output_file = Path("results/load_test_results.csv")
#     output_file.parent.mkdir(parents=True, exist_ok=True)

#     fieldnames = [
#         "request_id",
#         "scenario",
#         "status",
#         "response_time",
#         "response",
#         "total_execution_time"
#     ]

#     with output_file.open(
#         "w",
#         newline="",
#         encoding="utf-8"
#     ) as file:

#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(all_results)

#     print("\n" + "=" * 60)
#     print("ALL LOAD TESTS COMPLETED")
#     print("=" * 60)
#     print("Total Requests:", len(all_results))
#     print("Results saved to:", output_file)


# if __name__ == "__main__":
#     run_all_load_tests()







import time
import csv
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from simulator.standin_model import StandInModel


def run_single_request(model, request_id, scenario):
    """Execute one simulated request and record its result."""

    request_start_time = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    start_time = time.perf_counter()

    try:
        response = model.generate(
            f"{scenario} research question {request_id}"
        )
        status = "SUCCESS"

    except Exception as error:
        response = str(error)
        status = "FAILED"

    end_time = time.perf_counter()

    return {
        "request_id": request_id,
        "scenario": scenario,
        "start_time": request_start_time,
        "status": status,
        "response_time": round(end_time - start_time, 4),
        "response": response,
        "retries": 0,
        "source": "standin",
        "first_token_ms": "",
        "tokens_in": "",
        "tokens_out": "",
        "retrieval_setting": "",
        "answer_grade": ""
    }


def run_scenario(scenario, total_requests, max_workers, response_delay=1):
    """Run one load-test scenario."""

    print("\n" + "=" * 60)
    print(f"SCENARIO: {scenario}")
    print("=" * 60)

    model = StandInModel(
        model_name="TheRelay-StandIn",
        response_delay=response_delay,
        failure_rate=0.0
    )

    results = []
    overall_start = time.perf_counter()

    print("Total Requests:", total_requests)
    print("Concurrent Workers:", max_workers)
    print("Response Delay:", response_delay, "seconds")
    print("\nRunning...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        futures = [
            executor.submit(
                run_single_request,
                model,
                request_id,
                scenario
            )
            for request_id in range(1, total_requests + 1)
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            print(
                f"Request {result['request_id']}: "
                f"{result['status']} | "
                f"Time: {result['response_time']} seconds"
            )

    total_time = time.perf_counter() - overall_start

    successful = sum(
        result["status"] == "SUCCESS"
        for result in results
    )

    failed = total_requests - successful

    response_times = sorted(
        result["response_time"] for result in results
    )

    average_time = sum(response_times) / len(response_times)

    def percentile(values, percentile_value):
        index = round((len(values) - 1) * percentile_value / 100)
        return values[index]

    print("\n--- Scenario Results ---")
    print("Successful:", successful)
    print("Failed:", failed)
    print("Average Latency:", round(average_time, 4), "seconds")
    print("Median Latency:", round(percentile(response_times, 50), 4))
    print("P95 Latency:", round(percentile(response_times, 95), 4))
    print("P99 Latency:", round(percentile(response_times, 99), 4))
    print("Total Execution Time:", round(total_time, 4), "seconds")

    for result in results:
        result["total_execution_time"] = round(total_time, 4)

    return results


def run_all_load_tests():

    all_results = []

    # Scenario 1: Steady Load
    steady_results = run_scenario(
        scenario="steady_load",
        total_requests=10,
        max_workers=2,
        response_delay=1
    )
    all_results.extend(steady_results)

    # Scenario 2: Burst Load
    burst_results = run_scenario(
        scenario="burst_load",
        total_requests=15,
        max_workers=15,
        response_delay=1
    )
    all_results.extend(burst_results)

    # Scenario 3: Sustained Overload
    overload_results = run_scenario(
        scenario="sustained_overload",
        total_requests=20,
        max_workers=5,
        response_delay=2
    )
    all_results.extend(overload_results)

    # Save the original detailed load-test results
    detailed_file = Path("results/load_test_results.csv")
    detailed_file.parent.mkdir(parents=True, exist_ok=True)

    all_results.sort(
        key=lambda item: (
            item["scenario"],
            item["request_id"]
        )
    )

    detailed_fields = [
        "request_id",
        "scenario",
        "status",
        "response_time",
        "response",
        "total_execution_time"
    ]

    with detailed_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=detailed_fields
        )
        writer.writeheader()

        for result in all_results:
            writer.writerow({
                field: result.get(field, "")
                for field in detailed_fields
            })

    # Create assignment-required results.csv
    assignment_file = Path("results/results.csv")

    assignment_fields = [
        "request_id",
        "scenario",
        "source",
        "start_time",
        "first_token_ms",
        "total_ms",
        "status",
        "retries",
        "tokens_in",
        "tokens_out",
        "retrieval_setting",
        "answer_grade"
    ]

    with assignment_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=assignment_fields
        )
        writer.writeheader()

        for result in all_results:
            writer.writerow({
                "request_id": result["request_id"],
                "scenario": result["scenario"],
                "source": result["source"],
                "start_time": result["start_time"],
                "first_token_ms": result["first_token_ms"],
                "total_ms": round(
                    result["response_time"] * 1000, 2
                ),
                "status": result["status"],
                "retries": result["retries"],
                "tokens_in": result["tokens_in"],
                "tokens_out": result["tokens_out"],
                "retrieval_setting": result["retrieval_setting"],
                "answer_grade": result["answer_grade"]
            })

    print("\n" + "=" * 60)
    print("ALL LOAD TESTS COMPLETED")
    print("=" * 60)
    print("Total Requests:", len(all_results))
    print("Detailed Results:", detailed_file)
    print("Assignment Results:", assignment_file)


if __name__ == "__main__":
    run_all_load_tests()
