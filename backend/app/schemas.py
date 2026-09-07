from typing import List
from pydantic import BaseModel, Field


# ============================================================
# PS8 — Question Variation Request
# ============================================================

class VariationRequest(BaseModel):
    question: str = Field(..., min_length=10)
    num_variations: int = Field(..., ge=1, le=20)


class VariationResponse(BaseModel):
    seed_question: str
    requested_variations: int
    status: str


# ============================================================
# PS2 — AI Reliability Verification
# ============================================================

class VerifyRequest(BaseModel):
    question: str = Field(..., min_length=10)
    generated_answer: str = Field(..., min_length=1)
    reference_text: str = ""


class FlaggedSpan(BaseModel):
    text: str
    reason: str


class Contradiction(BaseModel):
    text: str
    reason: str


class UnsupportedClaim(BaseModel):
    text: str
    reason: str


class VerifyResponse(BaseModel):
    reliability_score: float
    hallucination_probability: float
    factual_consistency: float
    semantic_correctness: float
    verdict: str
    summary: str
    flagged_spans: List[FlaggedSpan]
    contradictions: List[Contradiction]
    unsupported_claims: List[UnsupportedClaim]