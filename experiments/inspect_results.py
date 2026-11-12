
import pandas as pd
from pathlib import Path

files = [
    "results.csv",
    "load_test_results.csv",
    "service_comparison.csv",
    "retrieval_comparison.csv",
    "answer_quality_review.csv",
    "manual_quality_grades.csv",
    "quality_test_results.csv"
]

for name in files:

    file_path = Path("results") / name

    print("\n" + "=" * 60)
    print("FILE:", name)
    print("=" * 60)

    if not file_path.exists():
        print("File not found!")
        continue

    df = pd.read_csv(file_path)

    print("Rows:", len(df))
    print("Columns:", list(df.columns))
