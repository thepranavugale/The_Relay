
import csv

from src.validator import validate_citations


INPUT_FILE = "results/answer_quality_review.csv"
OUTPUT_FILE = "results/answer_quality_review.csv"


def parse_sources(source_text):
    sources = []

    if not source_text:
        return sources

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
    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    updated_count = 0

    for row in rows:
        if row.get("status", "").lower() != "success":
            continue

        sources = parse_sources(row.get("source_papers", ""))

        validation = validate_citations(
            row.get("answer", ""),
            sources
        )

        row["citation_valid"] = str(
            validation["citation_valid"]
        )

        updated_count += 1

        print(
            f'{row["question_id"]}: '
            f'Citation Valid = {validation["citation_valid"]}'
        )

    if rows:
        fieldnames = list(rows[0].keys())

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(rows)

    print("\n--- Revalidation Summary ---")
    print("Total rows:", len(rows))
    print("Successfully revalidated:", updated_count)

    valid_count = sum(
        row.get("citation_valid", "").lower() == "true"
        for row in rows
        if row.get("status", "").lower() == "success"
    )

    print("Valid citations:", valid_count)
    print("Invalid or missing citations:", updated_count - valid_count)


if __name__ == "__main__":
    main()
