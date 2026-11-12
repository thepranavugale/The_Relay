
import os
import pandas as pd


INPUT_FILE = "results/answer_quality_review.csv"
OUTPUT_FILE = "results/manual_quality_grades.csv"


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "question_id",
        "question",
        "answer",
        "source_papers"
    ]

    for column in required_columns:
        if column not in df.columns:
            print(f"Missing required column: {column}")
            return

    os.makedirs("results", exist_ok=True)

    if os.path.exists(OUTPUT_FILE):
        grades_df = pd.read_csv(OUTPUT_FILE)
    else:
        grades_df = pd.DataFrame(columns=[
            "question_id",
            "manual_grade",
            "review_notes"
        ])

    completed_ids = set(grades_df["question_id"].astype(str))

    for _, row in df.iterrows():
        question_id = str(row["question_id"])

        if question_id in completed_ids:
            continue

        print("\n" + "=" * 70)
        print(f"Question ID: {question_id}")
        print("\nQUESTION:")
        print(row["question"])

        print("\nANSWER:")
        print(row["answer"])

        print("\nRETRIEVED SOURCES:")
        print(row["source_papers"])

        print("\nGRADING RUBRIC:")
        print("2 = Correct and sufficiently supported")
        print("1 = Partially correct or incomplete")
        print("0 = Incorrect or unsupported")

        while True:
            grade = input("\nEnter manual grade (0/1/2): ").strip()

            if grade in ["0", "1", "2"]:
                break

            print("Invalid grade. Enter only 0, 1, or 2.")

        notes = input("Enter review notes: ").strip()

        new_row = pd.DataFrame([{
            "question_id": question_id,
            "manual_grade": int(grade),
            "review_notes": notes
        }])

        grades_df = pd.concat(
            [grades_df, new_row],
            ignore_index=True
        )

        grades_df.to_csv(OUTPUT_FILE, index=False)

        print(f"\nSaved grade for {question_id}.")

    print("\n" + "=" * 70)
    print("MANUAL QUALITY GRADING COMPLETED")

    print(f"Total graded questions: {len(grades_df)}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
