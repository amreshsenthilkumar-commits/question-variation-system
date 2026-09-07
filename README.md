# VOID WALKER — AI Assessment Generation & Reliability System

> **HackWithAMYPO 2026 | PS8 + PS2**

An AI-powered assessment system that combines **question variation generation** with **AI-generated content reliability analysis**.

The system is designed around a simple principle:

**Generate → Validate → Verify → Review**

Instead of treating an LLM's output as automatically trustworthy, the system generates diverse assessment content, validates the generated questions, and analyzes AI-generated content for reliability before instructor use.

---

## 🎯 Problem

Creating multiple versions of an assessment question manually is time-consuming.

Simply changing a few words does not create a meaningful variation. A useful variation should preserve:

- Learning objective
- Topic and key concepts
- Difficulty
- Cognitive operation
- Correctness

At the same time, AI-generated content can contain:

- Hallucinated facts
- Unsupported claims
- Contradictory statements
- Semantically incorrect information

Therefore, our solution combines **generation and reliability analysis** into one assessment workflow.

---

# 💡 Solution

VOID WALKER combines two problem statements:

### PS8 — Assignment Question Iteration & Variation Generation System

Generates meaningful variations of a seed question while attempting to preserve its learning objective, difficulty, and key concepts.

### PS2 — AI Hallucination Detection & Reliability Scoring System

Analyzes AI-generated content and produces:

- Reliability score
- Hallucination probability
- Factual consistency
- Semantic correctness
- Verdict
- Explainable flagged spans
- Contradictions
- Unsupported claims

---

# 🔄 System Workflow

```text
                    INSTRUCTOR
                        │
                        ▼
                 SEED QUESTION
                        │
                        ▼
               ┌─────────────────┐
               │  PS8 GENERATOR  │
               └────────┬────────┘
                        │
                        ▼
             QUESTION VARIATIONS
                        │
                        ▼
              VALIDATION LAYER
                        │
                        ▼
           GENERATED QUESTION CONTENT
                        │
                        ▼
               ┌─────────────────┐
               │ PS2 VERIFICATION│
               └────────┬────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      RELIABLE      UNCERTAIN      PROBLEMATIC
          │             │             │
          ▼             ▼             ▼
       ACCEPT         REVIEW       REGENERATE
                        │
                        ▼
                 INSTRUCTOR REVIEW