import json
import re

from ai.ollama_client import ask_ollama


# ============================================================
# JSON Extraction
# ============================================================

def extract_json(text: str):
    """
    Extract a JSON object from the LLM response.

    Handles:
    - plain JSON
    - ```json ... ```
    - additional text surrounding JSON
    """

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(
        r"```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```\s*",
        "",
        text
    )

    # Locate JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "No valid JSON object found in model response."
        )

    json_text = text[start:end + 1]

    return json.loads(json_text)


# ============================================================
# PS2 Reliability Verification
# ============================================================

def verify_content(
    question: str,
    generated_answer: str,
    reference_text: str = ""
):
    """
    Analyze AI-generated content.

    Evaluates:
    - factual consistency
    - semantic correctness
    - hallucination probability
    - unsupported claims
    - contradictions
    - overall reliability
    - explainable flagged spans
    """

    if reference_text.strip():
        reference_section = reference_text
    else:
        reference_section = (
            "No trusted reference text was provided. "
            "Do not claim that facts have been externally verified."
        )

    prompt = f"""
You are an AI reliability and hallucination detection system.

Your task is to analyze an AI-generated answer before it is shown
to a learner.

============================================================
QUESTION
============================================================

{question}

============================================================
AI-GENERATED ANSWER
============================================================

{generated_answer}

============================================================
TRUSTED REFERENCE
============================================================

{reference_section}

============================================================
ANALYSIS REQUIREMENTS
============================================================

Evaluate:

1. Factual consistency
2. Semantic correctness
3. Hallucination probability
4. Unsupported claims
5. Contradictory claims
6. Whether the answer addresses the question
7. Overall reliability
8. Explainable reasons for suspicious portions

IMPORTANT RULES:

- Do not assume an AI-generated statement is true simply because
  it sounds plausible.
- If no trusted reference is provided, do not pretend external
  verification occurred.
- Distinguish factual information from assumptions, opinions,
  and reasonable inferences.
- Flag meaningful problems only.
- Do not invent problems in a correct answer.
- Reliability score must be between 0 and 100.
- Hallucination probability must be between 0 and 1.
- Factual consistency must be between 0 and 1.
- Semantic correctness must be between 0 and 1.
- Use "unverifiable" when an important claim cannot be adequately
  established from the supplied information.
- Flag the exact suspicious portion of the answer whenever possible.
- Give a short and clear reason for every flagged span.

============================================================
VERDICT DEFINITIONS
============================================================

trustworthy:
The answer is well supported and contains no significant
factual or semantic problems.

partially reliable:
The answer is mostly useful but contains uncertainty,
minor unsupported claims, or limited issues.

misleading:
The answer contains significant incorrect or unsupported
information that could mislead the learner.

fabricated:
The answer contains clearly false or invented information.

unverifiable:
Important claims cannot be adequately verified from the
available reference information.

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "reliability_score": 0,
    "hallucination_probability": 0.0,
    "factual_consistency": 0.0,
    "semantic_correctness": 0.0,
    "verdict": "trustworthy",
    "summary": "Short explanation of the overall assessment.",
    "flagged_spans": [
        {{
            "text": "exact suspicious text",
            "reason": "Why this portion is suspicious or incorrect."
        }}
    ],
    "contradictions": [
        {{
            "text": "claim involved in contradiction",
            "reason": "Explanation of the contradiction."
        }}
    ],
    "unsupported_claims": [
        {{
            "text": "unsupported claim",
            "reason": "Why the claim cannot be established."
        }}
    ]
}}
"""

    response = ask_ollama(prompt)

    try:
        result = extract_json(response)

    except Exception as error:
        raise ValueError(
            f"Failed to parse reliability analysis: {error}\n"
            f"Raw model response:\n{response}"
        )

    # ========================================================
    # Basic Output Validation
    # ========================================================

    required_fields = [
        "reliability_score",
        "hallucination_probability",
        "factual_consistency",
        "semantic_correctness",
        "verdict",
        "summary",
        "flagged_spans",
        "contradictions",
        "unsupported_claims"
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"PS2 response missing required field: {field}"
            )

    # Clamp numerical values to valid ranges
    result["reliability_score"] = max(
        0,
        min(100, float(result["reliability_score"]))
    )

    result["hallucination_probability"] = max(
        0,
        min(1, float(result["hallucination_probability"]))
    )

    result["factual_consistency"] = max(
        0,
        min(1, float(result["factual_consistency"]))
    )

    result["semantic_correctness"] = max(
        0,
        min(1, float(result["semantic_correctness"]))
    )

    return result