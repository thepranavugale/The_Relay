
# from unittest.mock import MagicMock, patch

# from src.pipeline import TheRelayPipeline


# def test_pipeline_returns_answer():

#     fake_retriever = MagicMock()
#     fake_retriever.search.return_value = [
#         {
#             "paper": "Attention Is All You Need",
#             "page": 2,
#             "chunk": 1,
#             "text": "The Transformer uses attention mechanisms.",
#             "score": 0.9
#         }
#     ]

#     fake_groq = MagicMock()
#     fake_groq.generate.return_value = (
#         "The Transformer uses attention mechanisms. "
#         "[Attention Is All You Need, p. 2]"
#     )

#     with patch(
#         "src.pipeline.PaperRetriever",
#         return_value=fake_retriever
#     ), patch(
#         "src.pipeline.GroqClient",
#         return_value=fake_groq
#     ):

#         pipeline = TheRelayPipeline()
#         result = pipeline.ask("Explain Transformer architecture")

#     assert result is not None
#     assert isinstance(result, str)
#     assert len(result.strip()) > 0


# def test_pipeline_handles_empty_question():

#     pipeline = TheRelayPipeline()

#     result = pipeline.ask("")

#     assert result is not None













from unittest.mock import MagicMock, patch

import pytest

from src.pipeline import TheRelayPipeline


def test_pipeline_returns_answer():

    fake_retriever = MagicMock()

    fake_retriever.search.return_value = [
        {
            "paper": "Attention Is All You Need",
            "page": 2,
            "chunk": 1,
            "text": "The Transformer uses attention mechanisms.",
            "score": 0.9
        }
    ]

    fake_groq = MagicMock()

    fake_groq.generate_response.return_value = (
        "The Transformer uses attention mechanisms. "
        "[Attention Is All You Need, p. 2]"
    )

    with patch(
        "src.pipeline.PaperRetriever",
        return_value=fake_retriever
    ), patch(
        "src.pipeline.GroqClient",
        return_value=fake_groq
    ):

        pipeline = TheRelayPipeline()
        result = pipeline.ask("Explain Transformer architecture")

    assert isinstance(result, dict)
    assert isinstance(result["answer"], str)
    assert len(result["answer"].strip()) > 0


def test_pipeline_handles_empty_question():

    pipeline = TheRelayPipeline()

    with pytest.raises(ValueError, match="Question cannot be empty"):
        pipeline.ask("")


def test_pipeline_handles_whitespace_question():

    pipeline = TheRelayPipeline()

    with pytest.raises(ValueError, match="Question cannot be empty"):
        pipeline.ask("   ")
