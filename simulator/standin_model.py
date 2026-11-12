
import time
import random


class StandInModel:
    """
    Simulated AI model for testing The Relay
    without calling a real LLM API.
    """

    def __init__(
        self,
        model_name="TheRelay-StandIn",
        response_delay=1,
        failure_rate=0.0
    ):
        if response_delay < 0:
            raise ValueError("response_delay cannot be negative.")

        if not 0 <= failure_rate <= 1:
            raise ValueError("failure_rate must be between 0 and 1.")

        self.model_name = model_name
        self.response_delay = response_delay
        self.failure_rate = failure_rate

        self.request_count = 0

    def generate(self, prompt):
        """
        Simulate an AI model response.
        """

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        self.request_count += 1

        print(f"\n[{self.model_name}] Processing request...")
        time.sleep(self.response_delay)

        # Simulate occasional API failures
        if random.random() < self.failure_rate:
            raise ConnectionError(
                "Simulated model connection failure."
            )

        response = (
            "This is a simulated response from The Relay Stand-In Model.\n"
            f"Your prompt was: {prompt[:300]}\n"
            "Note: This response is generated for testing only, "
            "not by a real AI model."
        )

        print(f"[{self.model_name}] Response generated.")

        return response

    def get_request_count(self):
        """Return the total number of requests."""
        return self.request_count


# ---------------------------------------
# TEST FUNCTION
# ---------------------------------------

def main():

    print("=" * 45)
    print("THE RELAY - STAND-IN MODEL TEST")
    print("=" * 45)

    model = StandInModel(
        model_name="TheRelay-StandIn",
        response_delay=1,
        failure_rate=0.0
    )

    test_prompt = (
        "Explain the main idea of the Attention Is All You Need paper."
    )

    try:
        response = model.generate(test_prompt)

        print("\nModel Response:")
        print(response)

        print("\nTotal Requests:", model.get_request_count())

    except Exception as error:
        print("\nModel Error:", error)


if __name__ == "__main__":
    main()
