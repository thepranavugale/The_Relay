
import csv
from src.validator import validate_citations


FILE_PATH = "results/answer_quality_review.csv"


def parse_sources(source_text):
    sources = []

    for item in source_text.split("; "):
        if " (p. " not in item:
            continue

        paper, page_part = item.rsplit(" (p. ", 1)

        try:
            page = int(page_part.rstrip(")"))

            sources.append({
                "paper": paper,
                "page": page
            })

        except ValueError:
            continue

    return sources


def main():
    with open(
        FILE_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        rows = list(csv.DictReader(file))

    print("\n--- INVALID CITATION DETAILS ---")

    for row in rows:

        if row.get("status", "").lower() != "success":
            continue

        sources = parse_sources(
            row.get("source_papers", "")
        )

        validation = validate_citations(
            row.get("answer", ""),
            sources
        )

        if not validation["citation_valid"]:

            print("\nQuestion:", row["question_id"])
            print("Question Text:", row["question"])
            print("Citations:", validation["citations"])
            print("Invalid:", validation["invalid_citations"])
            print("Retrieved Sources:", sources)

    print("\n--- INSPECTION COMPLETED ---")


if __name__ == "__main__":
    main()
