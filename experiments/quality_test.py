
import csv
import time
from pathlib import Path

from simulator.standin_model import StandInModel


def run_quality_test():

    print("=" * 55)
    print("THE RELAY - QUALITY TEST")
    print("=" * 55)

    model = StandInModel(
        model_name="TheRelay-StandIn",
        response_delay=0,
        failure_rate=0.0
    )

    test_cases = [
        "Explain the Transformer architecture.",
        "What is self-attention?",
        "Explain multi-head attention.",
        "What is the purpose of positional encoding?",
        "Explain scaled dot-product attention."
    ]

    results = []

    for number, question in enumerate(test_cases, start=1):

        print(f"\nTest Case {number}")
        print("Question:", question)

        start_time = time.perf_counter()

        try:
            response = model.generate(question)

            response_time = time.perf_counter() - start_time

            passed = (
                isinstance(response, str)
                and len(response.strip()) > 0
                and "simulated response" in response.lower()
            )

            status = "PASS" if passed else "FAIL"

        except Exception as error:

            response = str(error)
            response_time = time.perf_counter() - start_time
            status = "FAIL"

        print("Status:", status)
        print("Response Time:", round(response_time, 4), "seconds")

        results.append({
            "test_id": number,
            "question": question,
            "status": status,
            "response_time": round(response_time, 4),
            "response": response
        })

    passed_count = sum(
        result["status"] == "PASS"
        for result in results
    )

    failed_count = len(results) - passed_count

    print("\n" + "=" * 55)
    print("QUALITY TEST RESULTS")
    print("=" * 55)

    print("Total Test Cases:", len(results))
    print("Passed:", passed_count)
    print("Failed:", failed_count)

    quality_score = (passed_count / len(results)) * 100

    print("Quality Score:", round(quality_score, 2), "%")

    output_file = Path("results/quality_test_results.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "test_id",
                "question",
                "status",
                "response_time",
                "response"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nResults saved to:", output_file)
    print("\nQUALITY TEST COMPLETED!")


if __name__ == "__main__":
    run_quality_test()
