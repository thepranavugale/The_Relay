# import csv
# import time
# from pathlib import Path

# from src.pipeline import TheRelayPipeline
# from experiments.quality_questions import QUALITY_QUESTIONS


# OUTPUT_FILE = Path("results/answer_quality_review.csv")


# def main():
#     print("=" * 60)
#     print("THE RELAY - ANSWER QUALITY EVALUATION")
#     print("=" * 60)

#     # Pipeline एकदाच initialize करतो.
#     pipeline = TheRelayPipeline(top_k=4)

#     OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

#     fieldnames = [
#         "question_id",
#         "question",
#         "expected_topic",
#         "answer",
#         "source_papers",
#         "citation_valid",
#         "total_ms",
#         "status",
#         "answer_grade",
#         "review_notes",
#     ]

#     rows = []

#     for index, item in enumerate(QUALITY_QUESTIONS, start=1):
#         question_id = item["id"]
#         question = item["question"]
#         expected_topic = item["expected_topic"]

#         print(f"\n[{index}/{len(QUALITY_QUESTIONS)}] {question}")
#         start_time = time.perf_counter()

#         try:
#             result = pipeline.ask(question)
#             total_ms = round((time.perf_counter() - start_time) * 1000, 2)

#             answer = result.get("answer", "")
#             sources = result.get("sources", [])
#             validation = result.get("validation", {})

#             source_details = []
#             for source in sources:
#                 paper = source.get("paper", "Unknown paper")
#                 page = source.get("page", "Unknown page")
#                 source_details.append(f"{paper} (p. {page})")

#             source_papers = "; ".join(source_details)

#             if isinstance(validation, dict):
#                 citation_valid = validation.get(
#                     "valid",
#                     validation.get("is_valid", "")
#                 )
#             else:
#                 citation_valid = validation

#             rows.append({
#                 "question_id": question_id,
#                 "question": question,
#                 "expected_topic": expected_topic,
#                 "answer": answer,
#                 "source_papers": source_papers,
#                 "citation_valid": citation_valid,
#                 "total_ms": total_ms,
#                 "status": "success",
#                 "answer_grade": "",
#                 "review_notes": "",
#             })

#             print(f"Status: SUCCESS")
#             print(f"Response time: {total_ms} ms")
#             print(f"Citation validation: {citation_valid}")
#             print(f"Answer preview: {str(answer)[:250]}")

#         except Exception as error:
#             total_ms = round((time.perf_counter() - start_time) * 1000, 2)

#             rows.append({
#                 "question_id": question_id,
#                 "question": question,
#                 "expected_topic": expected_topic,
#                 "answer": "",
#                 "source_papers": "",
#                 "citation_valid": "",
#                 "total_ms": total_ms,
#                 "status": f"failed: {error}",
#                 "answer_grade": "",
#                 "review_notes": "",
#             })

#             print(f"Status: FAILED - {error}")

#     with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as csv_file:
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)

#     successful = sum(1 for row in rows if row["status"] == "success")
#     failed = len(rows) - successful

#     print("\n" + "=" * 60)
#     print("EVALUATION SUMMARY")
#     print("=" * 60)
#     print(f"Total questions: {len(rows)}")
#     print(f"Successful: {successful}")
#     print(f"Failed: {failed}")
#     print(f"CSV saved to: {OUTPUT_FILE}")


# if __name__ == "__main__":
#     main()








import csv
import time
from pathlib import Path

from src.pipeline import TheRelayPipeline
from experiments.quality_questions import QUALITY_QUESTIONS


OUTPUT_FILE = Path("results/answer_quality_review.csv")


def main():
    print("=" * 60)
    print("THE RELAY - ANSWER QUALITY EVALUATION")
    print("=" * 60)

    pipeline = TheRelayPipeline(top_k=4)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "question_id",
        "question",
        "expected_topic",
        "answer",
        "source_papers",
        "citation_valid",
        "total_ms",
        "status",
        "answer_grade",
        "review_notes",
    ]

    rows = []

    for index, item in enumerate(QUALITY_QUESTIONS, start=1):
        question_id = item["id"]
        question = item["question"]
        expected_topic = item["expected_topic"]

        print(f"\n[{index}/{len(QUALITY_QUESTIONS)}] {question}")

        start_time = time.perf_counter()

        try:
            result = pipeline.ask(question)

            total_ms = round(
                (time.perf_counter() - start_time) * 1000, 2
            )

            answer = result.get("answer", "")
            sources = result.get("sources", [])
            validation = result.get("validation")

            source_details = []

            for source in sources:
                paper = source.get("paper", "Unknown paper")
                page = source.get("page", "Unknown page")
                source_details.append(f"{paper} (p. {page})")

            source_papers = "; ".join(source_details)

            if isinstance(validation, dict):
                citation_valid = validation.get(
                    "citation_valid", ""
                )
            else:
                citation_valid = ""

            rows.append({
                "question_id": question_id,
                "question": question,
                "expected_topic": expected_topic,
                "answer": answer,
                "source_papers": source_papers,
                "citation_valid": citation_valid,
                "total_ms": total_ms,
                "status": "success",
                "answer_grade": "",
                "review_notes": "",
            })

            print("Status: SUCCESS")
            print(f"Response time: {total_ms} ms")
            print(f"Citation validation: {citation_valid}")
            print(f"Answer preview: {str(answer)[:250]}")

        except Exception as error:
            total_ms = round(
                (time.perf_counter() - start_time) * 1000, 2
            )

            rows.append({
                "question_id": question_id,
                "question": question,
                "expected_topic": expected_topic,
                "answer": "",
                "source_papers": "",
                "citation_valid": "",
                "total_ms": total_ms,
                "status": f"failed: {error}",
                "answer_grade": "",
                "review_notes": "",
            })

            print(f"Status: FAILED - {error}")

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8-sig"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=fieldnames
        )
        writer.writeheader()
        writer.writerows(rows)

    successful = sum(
        1 for row in rows if row["status"] == "success"
    )
    failed = len(rows) - successful

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total questions: {len(rows)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"CSV saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
