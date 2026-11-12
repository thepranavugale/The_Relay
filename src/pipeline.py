
# from src.retriever import Retriever
# from src.groq_client import GroqClient
# from src.validator import (
#     validate_citations,
#     display_validation
# )
# from src.logger import logger


# class TheRelayPipeline:
#     """
#     Main pipeline connecting retrieval,
#     Groq generation and citation validation.
#     """

#     def __init__(self, top_k=5):

#         self.retriever = Retriever()
#         self.groq_client = GroqClient()
#         self.top_k = top_k

#         logger.info("The Relay pipeline initialized.")

#     def ask(self, question):

#         if not isinstance(question, str) or not question.strip():
#             raise ValueError("Question cannot be empty.")

#         logger.info("New question received.")

#         # STEP 1: Retrieve relevant paper chunks
#         retrieved_chunks = self.retriever.retrieve(
#             question,
#             top_k=self.top_k
#         )

#         if not retrieved_chunks:
#             return {
#                 "question": question,
#                 "answer": "No relevant research paper content found.",
#                 "sources": [],
#                 "validation": None
#             }

#         # STEP 2: Prepare context
#         context_parts = []

#         for chunk in retrieved_chunks:

#             paper = chunk.get("paper", "Unknown Paper")
#             page = chunk.get("page", "Unknown")
#             content = chunk.get("text", "")

#             context_parts.append(
#                 f"[{paper}, p. {page}]\n{content}"
#             )

#         context = "\n\n".join(context_parts)

#         # STEP 3: Create prompt
#         prompt = f"""
# Answer the user's question using ONLY the
# research paper context provided below.

# Question:
# {question}

# Research Paper Context:
# {context}

# Instructions:
# 1. Give a clear and accurate answer.
# 2. Do not invent facts.
# 3. Use citations in this exact format:
#    [Paper Name, p. N]
# 4. Cite the paper and page supporting each claim.
# 5. If the context does not contain enough information,
#    clearly say that the information is unavailable.
# """

#         # STEP 4: Generate answer using Groq
#         logger.info("Generating answer using Groq.")

#         answer = self.groq_client.generate_response(
#             prompt=prompt,
#             system_message=(
#                 "You are The Relay, an academic research assistant. "
#                 "Answer using the supplied research context and "
#                 "provide accurate page citations."
#             )
#         )

#         # STEP 5: Validate citations
#         validation = validate_citations(
#             answer,
#             retrieved_chunks
#         )

#         logger.info("Citation validation completed.")

#         return {
#             "question": question,
#             "answer": answer,
#             "sources": retrieved_chunks,
#             "validation": validation
#         }

#     def display_result(self, result):

#         print("\n" + "=" * 55)
#         print("THE RELAY - FINAL ANSWER")
#         print("=" * 55)

#         print("\nQuestion:")
#         print(result["question"])

#         print("\nAnswer:")
#         print(result["answer"])

#         print("\nCitation Validation:")

#         if result["validation"] is not None:
#             display_validation(result["validation"])
#         else:
#             print("Validation not performed.")

#         print("\n" + "=" * 55)


# # ---------------------------------------
# # MAIN FUNCTION
# # ---------------------------------------

# def main():

#     print("=" * 55)
#     print("THE RELAY - PIPELINE TEST")
#     print("=" * 55)

#     try:

#         pipeline = TheRelayPipeline(top_k=5)

#         question = input(
#             "\nEnter your research question: "
#         ).strip()

#         result = pipeline.ask(question)

#         pipeline.display_result(result)

#     except Exception as error:

#         logger.exception("Pipeline execution failed.")

#         print("\nPipeline Error:")
#         print(error)


# if __name__ == "__main__":
#     main()









from src.retriever import PaperRetriever
from src.groq_client import GroqClient

from src.validator import (
    validate_citations,
    display_validation
)

from src.logger import logger


class TheRelayPipeline:

    def __init__(self, top_k=5):

        self.retriever = PaperRetriever()
        self.groq_client = GroqClient()
        self.top_k = top_k

        logger.info(
            "The Relay pipeline initialized."
        )

    def ask(self, question):

        if not isinstance(question, str) or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        logger.info(
            "New question received."
        )

        # STEP 1: Retrieve relevant chunks

        retrieved_chunks = self.retriever.search(
            query=question,
            k=self.top_k
        )

        if not retrieved_chunks:

            return {
                "question": question,
                "answer": "No relevant research paper content found.",
                "sources": [],
                "validation": None
            }

        # STEP 2: Prepare research context

        context_parts = []

        for chunk in retrieved_chunks:

            paper = chunk.get(
                "paper",
                "Unknown Paper"
            )

            page = chunk.get(
                "page",
                "Unknown"
            )

            content = chunk.get(
                "text",
                ""
            )

            context_parts.append(
                f"[{paper}, p. {page}]\n{content}"
            )

        context = "\n\n".join(context_parts)

        # STEP 3: Prepare prompt

        prompt = f"""
Answer the user's question using ONLY the
research paper context provided below.

Question:
{question}

Research Paper Context:
{context}

Instructions:
1. Give a clear and accurate answer.
2. Do not invent facts.
3. Use citations in this exact format:
   [Paper Name, p. N]
4. Cite the paper and page supporting each claim.
5. If the context does not contain enough information,
   clearly say that the information is unavailable.
"""

        # STEP 4: Generate answer using Groq

        logger.info(
            "Generating answer using Groq."
        )

        answer = self.groq_client.generate_response(
            prompt=prompt,
            system_message=(
                "You are The Relay, an academic research assistant. "
                "Answer using the supplied research context and "
                "provide accurate page citations."
            )
        )

        # STEP 5: Validate citations

        validation = validate_citations(
            answer,
            retrieved_chunks
        )

        logger.info(
            "Citation validation completed."
        )

        return {
            "question": question,
            "answer": answer,
            "sources": retrieved_chunks,
            "validation": validation
        }

    def display_result(self, result):

        print("\n" + "=" * 55)

        print(
            "THE RELAY - FINAL ANSWER"
        )

        print("=" * 55)

        print("\nQuestion:")

        print(
            result["question"]
        )

        print("\nAnswer:")

        print(
            result["answer"]
        )

        print("\nCitation Validation:")

        if result["validation"] is not None:

            display_validation(
                result["validation"]
            )

        else:

            print(
                "Validation not performed."
            )

        print("\n" + "=" * 55)


def main():

    print("=" * 55)

    print(
        "THE RELAY - PIPELINE TEST"
    )

    print("=" * 55)

    try:

        pipeline = TheRelayPipeline(
            top_k=5
        )

        question = input(
            "\nEnter your research question: "
        ).strip()

        result = pipeline.ask(
            question
        )

        pipeline.display_result(
            result
        )

    except Exception as error:

        logger.exception(
            "Pipeline execution failed."
        )

        print("\nPipeline Error:")
        print(error)


if __name__ == "__main__":
    main()
