
import requests

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_BASE_URL,
    REQUEST_TIMEOUT_SECONDS
)

from src.retry_manager import retry
from src.logger import logger


class GroqClient:
    """
    Client for communicating with the Groq API.
    """

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. Check your .env file."
            )

        self.api_url = (
            GROQ_BASE_URL.rstrip("/") + "/chat/completions"
        )

        self.model = GROQ_MODEL

        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        logger.info("Groq client initialized.")

    @retry(max_retries=2, base_delay=1, max_delay=5,
           retryable_exceptions=(requests.RequestException,))
    def generate_response(self, prompt, system_message=None):
        """
        Send a prompt to Groq and return the AI response.
        """

        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        messages = []

        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1500
        }

        logger.info("Sending request to Groq API.")

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS
        )

        # Raise an exception for HTTP errors
        response.raise_for_status()

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        logger.info("Groq API response received successfully.")

        return answer


# ---------------------------------------
# TEST FUNCTION
# ---------------------------------------

def main():

    print("=" * 45)
    print("THE RELAY - GROQ CLIENT TEST")
    print("=" * 45)

    try:
        client = GroqClient()

        prompt = (
            "Explain the Transformer architecture "
            "in simple words."
        )

        answer = client.generate_response(
            prompt=prompt,
            system_message=(
                "You are a helpful research assistant."
            )
        )

        print("\nGroq AI Response:")
        print(answer)

    except Exception as error:
        logger.exception("Groq client test failed.")
        print("\nError:", error)


if __name__ == "__main__":
    main()
