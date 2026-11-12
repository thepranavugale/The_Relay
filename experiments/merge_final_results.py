
import pandas as pd
from pathlib import Path

results_path = Path("results/results.csv")
quality_path = Path("results/answer_quality_review.csv")
grades_path = Path("results/manual_quality_grades.csv")

required_columns = [
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

# Read existing load-test results
load_df = pd.read_csv(results_path)

# Read quality evaluation and manual grades
quality_df = pd.read_csv(quality_path)
grades_df = pd.read_csv(grades_path)

# Combine quality results with manual grades
quality_df = quality_df.merge(
    grades_df[["question_id", "manual_grade"]],
    on="question_id",
    how="left"
)

# Prepare quality records in assignment format
quality_records = pd.DataFrame({
    "request_id": quality_df["question_id"],
    "scenario": "quality_evaluation",
    "source": "groq",
    "start_time": "",
    "first_token_ms": "",
    "total_ms": quality_df["total_ms"],
    "status": quality_df["status"].str.upper(),
    "retries": "",
    "tokens_in": "",
    "tokens_out": "",
    "retrieval_setting": "top_k=4",
    "answer_grade": quality_df["manual_grade"]
})

# Ensure exact assignment columns
load_df = load_df[required_columns]
quality_records = quality_records[required_columns]

# Combine records
combined_df = pd.concat(
    [load_df, quality_records],
    ignore_index=True
)

# Check duplicate request IDs within scenario
duplicates = combined_df.duplicated(
    subset=["request_id", "scenario"]
).sum()

if duplicates > 0:
    raise ValueError(
        f"Found {duplicates} duplicate request records. File not updated."
    )

# Save consolidated results
combined_df.to_csv(results_path, index=False)

print("Final results.csv created successfully!")
print("\nTotal records:", len(combined_df))
print("\nRecords by scenario:")
print(combined_df.groupby("scenario").size())

print("\nManual answer grade distribution:")
print(
    combined_df[
        combined_df["scenario"] == "quality_evaluation"
    ]["answer_grade"].value_counts().sort_index()
)

print("\nMissing values:")
print(combined_df.isna().sum())

print("\nFinal columns:")
print(combined_df.columns.tolist())

