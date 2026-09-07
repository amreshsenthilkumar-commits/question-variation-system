import json
import re

from ai.ollama_client import ask_ollama
from ai.similarity_checker import (
    calculate_similarity,
    is_too_similar
)


MAX_REGENERATION_ATTEMPTS = 3


def is_valid_variation(variation: dict, analysis: dict) -> bool:
    """
    Basic rule-based validation for generated variations.
    """

    question = variation.get("question", "").strip().lower()

    if not question:
        return False

    question_type = analysis.get(
        "question_type",
        "General"
    ).lower()

    # Reject cognitive-operation drift
    if question_type == "explanation":

        forbidden_patterns = [
            r"\bcompare\b",
            r"\bcomparison\b",
            r"\bdifferentiate\b",
            r"\bdistinguish\b",
            r"\bevaluate\b",
            r"\bevaluation\b",
            r"\banalyze\b",
            r"\banalysis\b",
            r"\bdesign\b",
            r"\badvantages and disadvantages\b",
            r"\bpros and cons\b",
        ]

        for pattern in forbidden_patterns:

            if re.search(pattern, question):
                return False

    # Make sure important concepts remain present
    key_concepts = analysis.get(
        "key_concepts",
        []
    )

    if key_concepts:

        concept_found = any(
            concept.lower() in question
            for concept in key_concepts
        )

        if not concept_found:
            return False

    return True


def build_prompt(
    question: str,
    num_variations: int,
    analysis: dict,
    previous_questions: list
) -> str:
    """
    Build the LLM prompt for generating variations.
    """

    topic = analysis.get(
        "topic",
        "General"
    )

    question_type = analysis.get(
        "question_type",
        "General"
    )

    difficulty = analysis.get(
        "difficulty",
        "Medium"
    )

    key_concepts = analysis.get(
        "key_concepts",
        []
    )

    learning_objective = (
        f"{question_type}: {question}"
    )

    previous_section = ""

    if previous_questions:

        previous_section = f"""
==================================================
QUESTIONS ALREADY GENERATED
==================================================

Do NOT repeat or closely paraphrase these questions:

{json.dumps(previous_questions, indent=2)}

Create NEW variations that are meaningfully different.
"""

    prompt = f"""
You are an expert university examination question designer.

Your task is to generate meaningful variations of ONE seed question.

SEED QUESTION:
{question}

TOPIC:
{topic}

COGNITIVE OPERATION:
{question_type}

DIFFICULTY:
{difficulty}

KEY CONCEPTS:
{key_concepts}

LEARNING OBJECTIVE:
{learning_objective}

{previous_section}

==================================================
CRITICAL RULE
==================================================

DO NOT change the cognitive operation.

If the seed is an EXPLANATION question, every variation must remain
an EXPLANATION question.

The student must still explain HOW something works, operates,
functions, or produces an outcome.

Do NOT convert an explanation question into:

- comparison
- evaluation
- analysis
- design
- advantages/disadvantages
- pros/cons
- listing
- definition
- prediction

==================================================
WHAT SHOULD CHANGE
==================================================

Create meaningful variations by changing:

- real-world scenario
- application context
- system situation
- practical context
- numerical values, when applicable

Do NOT merely replace words with synonyms.

Do NOT change the underlying concept being tested.

==================================================
QUALITY REQUIREMENTS
==================================================

Generate exactly {num_variations} NEW variations.

Each variation must:

1. Be a complete standalone academic question.
2. Preserve the same learning objective.
3. Preserve the same cognitive operation.
4. Preserve the same key concepts.
5. Preserve approximately the same difficulty.
6. Be meaningfully different from the seed.
7. Use a different scenario or context where possible.
8. NOT be a simple paraphrase.
9. NOT repeat previous questions.
10. NOT introduce a new primary learning objective.
11. NOT contain an answer or explanation.

Before returning the result, internally reject any variation
that violates these rules and replace it with a better variation.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Do not use markdown.

Use exactly this structure:

{{
    "variations": [
        {{
            "variation_id": 1,
            "question": "Complete standalone question",
            "changed_aspect": "Scenario or context changed",
            "learning_objective": "{learning_objective}",
            "cognitive_operation": "{question_type}",
            "difficulty": "{difficulty}"
        }}
    ]
}}
"""

    return prompt


def validate_candidates(
    question: str,
    candidates: list,
    analysis: dict,
    accepted_questions: list
) -> list:
    """
    Validate generated candidates using:
    1. Rule-based validation
    2. Similarity validation
    3. Duplicate detection
    """

    valid_variations = []

    for variation in candidates:

        variation_question = variation.get(
            "question",
            ""
        ).strip()

        if not variation_question:
            continue

        # -----------------------------------------
        # STEP 1: Rule validation
        # -----------------------------------------

        if not is_valid_variation(
            variation,
            analysis
        ):

            print(
                "Rejected variation: "
                "failed rule validation."
            )

            continue

        # -----------------------------------------
        # STEP 2: Duplicate detection
        # -----------------------------------------

        duplicate = False

        for previous_question in accepted_questions:

            previous_similarity = calculate_similarity(
                previous_question,
                variation_question
            )

            if previous_similarity >= 0.50:

                print(
                    "Rejected variation: "
                    "too similar to an existing variation."
                )

                duplicate = True
                break

        if duplicate:
            continue

        # -----------------------------------------
        # STEP 3: Similarity with seed
        # -----------------------------------------

        similarity_score = calculate_similarity(
            question,
            variation_question
        )

        print(
            f"Similarity score: {similarity_score}"
        )

        if is_too_similar(
            question,
            variation_question
        ):

            print(
                "Rejected variation because it is "
                f"too similar to the seed. "
                f"Score: {similarity_score}"
            )

            continue

        # -----------------------------------------
        # STEP 4: Accept variation
        # -----------------------------------------

        variation["similarity_score"] = (
            similarity_score
        )

        valid_variations.append(
            variation
        )

    return valid_variations


def generate_variations(
    question: str,
    num_variations: int,
    analysis: dict
) -> list:
    """
    Generate, validate and regenerate question variations
    until the requested number is reached or the maximum
    number of attempts is exhausted.
    """

    accepted_variations = []

    accepted_questions = []

    for attempt in range(
        1,
        MAX_REGENERATION_ATTEMPTS + 1
    ):

        remaining = (
            num_variations
            - len(accepted_variations)
        )

        if remaining <= 0:
            break

        print(
            f"\n========== GENERATION ATTEMPT "
            f"{attempt} =========="
        )

        print(
            f"Need {remaining} more variation(s)."
        )

        # -----------------------------------------
        # Build prompt
        # -----------------------------------------

        prompt = build_prompt(
            question,
            remaining,
            analysis,
            accepted_questions
        )

        # -----------------------------------------
        # Ask Ollama
        # -----------------------------------------

        response = ask_ollama(prompt)

        try:

            data = json.loads(response)

            candidates = data.get(
                "variations",
                []
            )

            # -----------------------------------------
            # Validate candidates
            # -----------------------------------------

            valid_variations = validate_candidates(
                question,
                candidates,
                analysis,
                accepted_questions
            )

            # -----------------------------------------
            # Add accepted variations
            # -----------------------------------------

            for variation in valid_variations:

                if len(
                    accepted_variations
                ) >= num_variations:
                    break

                variation["variation_id"] = (
                    len(accepted_variations) + 1
                )

                accepted_variations.append(
                    variation
                )

                accepted_questions.append(
                    variation["question"]
                )

            print(
                f"Accepted so far: "
                f"{len(accepted_variations)}/"
                f"{num_variations}"
            )

        except json.JSONDecodeError:

            print(
                "Warning: Ollama did not return "
                "valid JSON."
            )

            print(
                "Raw response:",
                response
            )

    # ---------------------------------------------
    # Final result
    # ---------------------------------------------

    if len(accepted_variations) < num_variations:

        print(
            "\nWARNING: Could not generate the "
            "requested number of valid variations "
            "within the maximum attempts."
        )

    return accepted_variations[:num_variations]