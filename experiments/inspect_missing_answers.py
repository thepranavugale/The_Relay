
import csv

FILE_PATH = "results/answer_quality_review.csv"

TARGET_QUESTIONS = ["Q04", "Q10", "Q15"]


def main():
    with open(
        FILE_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        rows = list(csv.DictReader(file))

    for row in rows:

        if row["question_id"] in TARGET_QUESTIONS:

            print("\n" + "=" * 70)
            print("QUESTION:", row["question_id"])
            print("QUESTION TEXT:", row["question"])
            print("STATUS:", row["status"])

            print("\n--- GENERATED ANSWER ---")
            print(row["answer"])

            print("\n--- SOURCE PAPERS ---")
            print(row["source_papers"])

            print("\n--- CITATION VALID ---")
            print(row["citation_valid"])

            print("=" * 70)


if __name__ == "__main__":
    main()
