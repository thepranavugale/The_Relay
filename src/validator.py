
import re


# Supports:
# [Paper Name, p. 5]
# [**Paper Name, p. 5**]
# 【Paper Name, p. 5】
# 【**Paper Name, p. 5**]

CITATION_PATTERN = re.compile(
    r"[\[【]\s*\**\s*([^\[\]【】]+?),\s*p\.\s*(\d+)\s*\**\s*[\]】]",
    re.IGNORECASE
)


def normalize_paper_name(name):
    name = str(name).casefold()

    # Remove invisible characters
    name = name.replace("\u200b", "")
    name = name.replace("\ufeff", "")

    # Normalize hyphen variations
    for character in ["-", "–", "—", "−", "‑"]:
        name = name.replace(character, "-")

    # Normalize whitespace
    name = " ".join(name.split())

    return name.strip()


def extract_citations(answer):
    citations = []

    if not answer:
        return citations

    matches = CITATION_PATTERN.findall(answer)

    for paper, page in matches:
        # Remove Markdown bold markers and extra spaces
        paper = paper.replace("*", "").strip()

        citations.append({
            "paper": paper,
            "page": int(page)
        })

    return citations


def validate_citations(answer, retrieved):
    citations = extract_citations(answer)

    allowed_sources = {
        (
            normalize_paper_name(item["paper"]),
            int(item["page"])
        )
        for item in retrieved
        if "paper" in item and "page" in item
    }

    valid_citations = []
    invalid_citations = []

    for citation in citations:
        paper_name = normalize_paper_name(citation["paper"])
        page_number = citation["page"]

        source_pair = (paper_name, page_number)

        citation_text = (
            f'[{citation["paper"]}, p. {page_number}]'
        )

        if source_pair in allowed_sources:
            valid_citations.append(citation_text)
        else:
            invalid_citations.append(citation_text)

    has_citation = len(citations) > 0

    citation_valid = (
        has_citation and len(invalid_citations) == 0
    )

    return {
        "has_citation": has_citation,
        "citation_valid": citation_valid,
        "invalid_citations": invalid_citations,
        "valid_citations": valid_citations,
        "citations": citations,
        "error": None
    }


def display_validation(result):
    print("\n--- Citation Validation ---")

    if result.get("error"):
        print("Error:", result["error"])
        return

    if not result.get("has_citation"):
        print("No citations found.")
        return

    print("Citation Valid:", result["citation_valid"])
    print("Valid Citations:", result["valid_citations"])
    print("Invalid Citations:", result["invalid_citations"])


def get_answer_grade(validation, answer):
    if not answer or not answer.strip():
        return "No Answer"

    if not validation.get("has_citation"):
        return "No Citation"

    if validation.get("citation_valid"):
        return "Citation Valid - Manual Review Needed"

    return "Invalid Citation"
