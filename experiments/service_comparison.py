
import csv
import time
from pathlib import Path
from datetime import datetime

from src.groq_client import GroqClient
from simulator.standin_model import StandInModel


PROMPT = (
    "Explain the main idea of Transformer architecture "
    "in simple words."
)


def measure_standin():

    model = StandInModel(
        model_name="TheRelay-StandIn",
        response_delay=1,
        failure_rate=0.0
    )

    start = time.perf_counter()

    try:
        answer = model.generate(PROMPT)
        status = "SUCCESS"
        error = ""

    except Exception as exception:
        answer = ""
        status = "FAILED"
        error = str(exception)

    total_ms = (time.perf_counter() - start) * 1000

    return {
        "source": "standin",
        "status": status,
        "total_ms": round(total_ms, 2),
        "response_length": len(answer),
        "error": error
    }


def measure_groq():

    start = time.perf_counter()

    try:
        client = GroqClient()
        answer = client.generate_response(
            prompt=PROMPT,
            system_message="You are a helpful research assistant."
        )

        status = "SUCCESS"
        error = ""

    except Exception as exception:
        answer = ""
        status = "FAILED"
        error = str(exception)

    total_ms = (time.perf_counter() - start) * 1000

    return {
        "source": "groq",
        "status": status,
        "total_ms": round(total_ms, 2),
        "response_length": len(answer),
        "error": error
    }


def main():

    print("=" * 55)
    print("THE RELAY - REAL SERVICE VS STAND-IN")
    print("=" * 55)

    results = []

    print("\nRunning Stand-in test...")
    results.append(measure_standin())

    print("\nRunning Groq API test...")
    results.append(measure_groq())

    print("\n" + "=" * 55)
    print("COMPARISON RESULTS")
    print("=" * 55)

    for result in results:

        print("\nSource:", result["source"])
        print("Status:", result["status"])
        print("Total Time:", result["total_ms"], "ms")
        print("Response Length:", result["response_length"])

        if result["error"]:
            print("Error:", result["error"])

    output_file = Path("results/service_comparison.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "timestamp",
        "source",
        "status",
        "total_ms",
        "response_length",
        "error"
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for result in results:
            writer.writerow({
                "timestamp": datetime.now().astimezone().isoformat(),
                **result
            })

    print("\nResults saved to:", output_file)


if __name__ == "__main__":
    main()
