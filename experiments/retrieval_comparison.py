
import time
import csv
from pathlib import Path

from src.retriever import PaperRetriever


def run_retrieval_comparison():

    print("========================================")
    print("THE RELAY - RETRIEVAL COMPARISON")
    print("========================================")

    retriever = PaperRetriever()

    test_queries = [
        "What is the main idea of attention in the Transformer architecture?",
        "How does self-attention work?",
        "What is multi-head attention?",
        "How does positional encoding work?",
        "What is dynamic chunking?"
    ]

    retrieval_settings = {
        "Setting_A_k2": 2,
        "Setting_B_k4": 4,
        "Setting_C_k8": 8
    }

    results = []

    for setting_name, k_value in retrieval_settings.items():

        print(f"\n\nTesting: {setting_name} (k={k_value})")
        print("----------------------------------------")

        for query_number, query in enumerate(test_queries, start=1):

            start_time = time.perf_counter()

            retrieved_chunks = retriever.search(
                query=query,
                k=k_value
            )

            retrieval_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

            total_characters = sum(
                len(chunk["text"])
                for chunk in retrieved_chunks
            )

            result = {
                "setting": setting_name,
                "k": k_value,
                "query_number": query_number,
                "query": query,
                "retrieved_chunks": len(retrieved_chunks),
                "retrieval_time_ms": round(retrieval_time_ms, 3),
                "context_characters": total_characters
            }

            results.append(result)

            print(
                f"Query {query_number}: "
                f"Chunks={len(retrieved_chunks)}, "
                f"Time={retrieval_time_ms:.3f} ms, "
                f"Characters={total_characters}"
            )

    output_file = Path("results/retrieval_comparison.csv")

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("\n========================================")
    print("RETRIEVAL COMPARISON COMPLETED")
    print("========================================")
    print("Total experiment records:", len(results))
    print("CSV saved to:", output_file)


if __name__ == "__main__":
    run_retrieval_comparison()
