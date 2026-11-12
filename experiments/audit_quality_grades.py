
import pandas as pd

answers = pd.read_csv(
    "results/answer_quality_review.csv"
)

grades = pd.read_csv(
    "results/manual_quality_grades.csv"
)

merged = answers.merge(
    grades[["question_id", "manual_grade", "review_notes"]],
    on="question_id",
    how="left",
    suffixes=("_answer", "_manual")
)

for _, row in merged.iterrows():

    print("\n" + "=" * 70)
    print("QUESTION:", row["question_id"])
    print(row["question"])

    print("\nACTUAL ANSWER:")
    print(row["answer"])

    print("\nSOURCE PAPERS:")
    print(row["source_papers"])

    print("\nSTATUS:", row["status"])
    print("CITATION VALID:", row["citation_valid"])
    print("ANSWER GRADE:", row["answer_grade"])

    print("\nMANUAL GRADE:", row["manual_grade"])
    print("MANUAL REVIEW NOTE:")
    print(row["review_notes_manual"])
