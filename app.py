
from src.pipeline import TheRelayPipeline
from src.logger import logger


def display_welcome():

    print("\n" + "=" * 60)
    print("          THE RELAY - AI RESEARCH ASSISTANT")
    print("=" * 60)

    print("\nWelcome to The Relay!")
    print("Ask questions based on your research papers.")
    print("\nType 'exit' or 'quit' to close the application.")

    print("=" * 60)


def main():

    display_welcome()

    try:

        # Initialize the main pipeline
        pipeline = TheRelayPipeline(top_k=5)

        logger.info("The Relay application started.")

        while True:

            question = input(
                "\nEnter your research question: "
            ).strip()

            # Exit condition
            if question.lower() in ["exit", "quit"]:
                print("\nThank you for using The Relay!")
                logger.info("Application closed by user.")
                break

            # Validate empty input
            if not question:
                print("Please enter a valid question.")
                continue

            try:

                print("\nProcessing your question...")
                print("Please wait...\n")

                # Get answer from pipeline
                result = pipeline.ask(question)

                # Display final answer
                pipeline.display_result(result)

            except Exception as error:

                logger.exception(
                    "Error while processing user question."
                )

                print("\nSomething went wrong:")
                print(error)

                print(
                    "\nPlease try again with another question."
                )

    except Exception as error:

        logger.exception(
            "Application initialization failed."
        )

        print("\nUnable to start The Relay:")
        print(error)


if __name__ == "__main__":
    main()
