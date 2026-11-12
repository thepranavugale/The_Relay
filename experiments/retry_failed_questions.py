
import csv
import time
from pathlib import Path
from time import perf_counter

from src.pipeline import TheRelayPipeline
from src.validator import get_answer_grade


CSV_FILE = Path("results/answer_quality_review.csv")

WAIT_BETWEEN_REQUESTS = 15


def main():
    with open(
        CSV_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    failed_rows = [
        row for row in rows
        if row.get("status", "").lower() != "success"
    ]

    print("Total questions:", len(rows))
    print("Questions to retry:", len(failed_rows))

    if not failed_rows:
        print("No failed questions found.")
        return

    pipeline = TheRelayPipeline(top_k=4)

    for index, row in enumerate(failed_rows):

        question_id = row["question_id"]

        print("\n" + "=" * 60)
        print(f"Retrying {question_id}: {row['question']}")

        if index > 0:
            print(
                f"Waiting {WAIT_BETWEEN_REQUESTS} seconds..."
            )
            time.sleep(WAIT_BETWEEN_REQUESTS)

        start = perf_counter()

        try:
            result = pipeline.ask(row["question"])

            total_ms = round(
                (perf_counter() - start) * 1000,
                2
            )

            answer = result.get("answer", "")
            sources = result.get("sources", [])
            validation = result.get("validation", {})

            source_text = "; ".join(
                f'{item["paper"]} (p. {item["page"]})'
                for item in sources
            )

            row["answer"] = answer
            row["source_papers"] = source_text
            row["citation_valid"] = str(
                validation.get("citation_valid", False)
            )
            row["total_ms"] = str(total_ms)
            row["status"] = "success"
            row["answer_grade"] = get_answer_grade(
                validation,
                answer
            )
            row["review_notes"] = ""

            print("Status: SUCCESS")
            print("Citation valid:", row["citation_valid"])
            print("Time:", total_ms, "ms")

        except Exception as error:
            total_ms = round(
                (perf_counter() - start) * 1000,
                2
            )

            row["status"] = "failed"
            row["total_ms"] = str(total_ms)
            row["review_notes"] = str(error)

            print("Status: FAILED")
            print("Error:", error)

        # Save after every question to protect previous results
        with open(
            CSV_FILE,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(rows[0].keys())
            )
            writer.writeheader()
            writer.writerows(rows)

    success_count = sum(
        row["status"].lower() == "success"
        for row in rows
    )

    failed_count = len(rows) - success_count

    print("\n" + "=" * 60)
    print("RETRY SUMMARY")
    print("Total questions:", len(rows))
    print("Successful:", success_count)
    print("Failed:", failed_count)
    print("CSV saved:", CSV_FILE)


if __name__ == "__main__":
    main()
