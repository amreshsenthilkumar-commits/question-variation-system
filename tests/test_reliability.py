from ai.reliability_analyzer import verify_content


question = "What is the working principle of CPU cache memory?"

generated_answer = """
CPU cache memory is a permanent storage device located inside the hard disk.
It stores files permanently even after the computer is switched off.
The cache is slower than RAM but has a much larger capacity than the hard disk.
"""

result = verify_content(
    question=question,
    generated_answer=generated_answer
)

print("\n========== PS2 RELIABILITY RESULT ==========\n")

print("Reliability Score:",
      result["reliability_score"])

print("Hallucination Probability:",
      result["hallucination_probability"])

print("Factual Consistency:",
      result["factual_consistency"])

print("Semantic Correctness:",
      result["semantic_correctness"])

print("Verdict:",
      result["verdict"])

print("\nSummary:")
print(result["summary"])

print("\nFlagged Spans:")
for item in result["flagged_spans"]:
    print("-", item["text"])
    print("  Reason:", item["reason"])

print("\nContradictions:")
for item in result["contradictions"]:
    print("-", item["text"])
    print("  Reason:", item["reason"])

print("\nUnsupported Claims:")
for item in result["unsupported_claims"]:
    print("-", item["text"])
    print("  Reason:", item["reason"])