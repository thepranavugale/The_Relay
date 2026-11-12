
from src.retriever import PaperRetriever


def run_retrieval_test():

    print("=" * 55)
    print("THE RELAY - RETRIEVAL TEST")
    print("=" * 55)

    retriever = PaperRetriever()

    test_queries = [
        "Transformer architecture",
        "Self-attention mechanism",
        "Multi-head attention",
        "Positional encoding",
        "Dynamic chunking"
    ]

    total_tests = len(test_queries)
    passed = 0

    for number, query in enumerate(test_queries, start=1):

        print(f"\nTest Case {number}")
        print("Query:", query)

        try:
            results = retriever.search(query, k=4)

            if results and len(results) > 0:
                status = "PASS"
                passed += 1

                print("Status:", status)
                print("Retrieved chunks:", len(results))

                for index, result in enumerate(results[:2], start=1):
                    print(f"\nResult {index}")
                    print("Paper:", result.get("paper", "Unknown"))
                    print("Page:", result.get("page", "Unknown"))
                    print("Score:", round(result.get("score", 0), 4))

            else:
                print("Status: FAIL")
                print("No relevant chunks retrieved.")

        except Exception as error:
            print("Status: FAIL")
            print("Error:", error)

    failed = total_tests - passed
    score = (passed / total_tests) * 100

    print("\n" + "=" * 55)
    print("RETRIEVAL TEST SUMMARY")
    print("=" * 55)

    print("Total Tests:", total_tests)
    print("Passed:", passed)
    print("Failed:", failed)
    print("Retrieval Success Rate:", round(score, 2), "%")

    print("\nRETRIEVAL TEST COMPLETED!")


if __name__ == "__main__":
    run_retrieval_test()
