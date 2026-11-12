
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import PROCESSED_DIR


class PaperRetriever:

    def __init__(self):

        self.chunks_file = PROCESSED_DIR / "chunks.jsonl"

        self.rows = []
        self.vectorizer = None
        self.tfidf_matrix = None

        self.load_chunks()
        self.build_index()

    def load_chunks(self):

        if not self.chunks_file.exists():
            raise FileNotFoundError(
                "chunks.jsonl not found! "
                "First run: python -m src.paper_loader"
            )

        print("\nLoading research paper chunks...")

        with self.chunks_file.open("r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    record = json.loads(line)

                    if not record.get("text", "").strip():
                        continue

                    self.rows.append(record)

                except json.JSONDecodeError as error:

                    raise ValueError(
                        f"Invalid JSON at line {line_number}: {error}"
                    )

        if not self.rows:
            raise ValueError(
                "No valid research paper chunks found!"
            )

        print(
            f"Loaded {len(self.rows)} chunks successfully."
        )

    def build_index(self):

        print("\nBuilding TF-IDF index...")

        documents = [
            row["text"] for row in self.rows
        ]

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50000,
            sublinear_tf=True
        )

        try:

            self.tfidf_matrix = self.vectorizer.fit_transform(
                documents
            )

        except ValueError as error:

            raise ValueError(
                "Unable to build TF-IDF index. "
                "Check whether your PDF files contain readable text."
            ) from error

        print("TF-IDF index created successfully.")

        print(
            "Vocabulary size:",
            len(self.vectorizer.vocabulary_)
        )

    def search(self, query, k=4):

        if not isinstance(query, str) or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        if not isinstance(k, int) or k < 1:
            raise ValueError(
                "k must be an integer of at least 1."
            )

        query_vector = self.vectorizer.transform(
            [query]
        )

        similarity_scores = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        ).ravel()

        ranked_indices = similarity_scores.argsort()[::-1]

        results = []

        for index in ranked_indices:

            score = float(similarity_scores[index])

            if score <= 0:
                break

            result = self.rows[index].copy()

            result["score"] = score

            results.append(result)

            if len(results) >= k:
                break

        return results

    def display_results(self, results):

        if not results:
            print(
                "\nNo relevant research information found."
            )
            return

        print("\n================================")
        print("RETRIEVAL SEARCH RESULTS")
        print("================================")

        for number, result in enumerate(results, start=1):

            print(f"\nResult {number}")
            print("------------------------------")

            print("Paper:", result["paper"])
            print("Page:", result["page"])
            print("Chunk:", result["chunk"])

            print(
                "Similarity Score:",
                round(result["score"], 4)
            )

            print("\nExtracted Text:")
            print(result["text"][:500])
            print("...")

            
def main():

    print("================================")
    print("THE RELAY - RETRIEVER MODULE")
    print("================================")

    retriever = PaperRetriever()

    question = (
        "What is the main idea of "
        "attention in the Transformer architecture?"
    )

    print("\nUser Question:")
    print(question)

    results = retriever.search(
        query=question,
        k=4
    )

    retriever.display_results(results)

    print("\n================================")
    print("RETRIEVAL TEST COMPLETED")
    print("================================")


if __name__ == "__main__":
    main()
