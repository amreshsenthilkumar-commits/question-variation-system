import re


def analyze_question(question: str) -> dict:
    """
    Analyze a seed question and extract basic educational properties.
    """

    text = question.strip()
    lower_text = text.lower()

    # -----------------------------
    # 1. Detect question type
    # -----------------------------
    if any(word in lower_text for word in [
        "explain", "describe", "discuss"
    ]):
        question_type = "Explanation"

    elif any(word in lower_text for word in [
        "compare", "differentiate", "distinguish"
    ]):
        question_type = "Comparison"

    elif any(word in lower_text for word in [
        "calculate", "compute", "find", "solve"
    ]):
        question_type = "Problem Solving"

    elif any(word in lower_text for word in [
        "define", "what is", "what are"
    ]):
        question_type = "Definition"

    elif any(word in lower_text for word in [
        "why", "reason"
    ]):
        question_type = "Reasoning"

    else:
        question_type = "General"

    # -----------------------------
    # 2. Estimate difficulty
    # -----------------------------
    if any(word in lower_text for word in [
        "design", "evaluate", "analyze", "justify",
        "derive", "optimize"
    ]):
        difficulty = "Hard"

    elif any(word in lower_text for word in [
        "explain", "compare", "differentiate",
        "describe", "calculate"
    ]):
        difficulty = "Medium"

    else:
        difficulty = "Easy"

    # -----------------------------
    # 3. Extract possible topic
    # -----------------------------
    topic = "General"

    topic_keywords = {
        "Computer Architecture": [
            "cpu", "cache", "processor", "memory",
            "register", "instruction"
        ],
        "Data Structures": [
            "array", "stack", "queue", "tree",
            "graph", "linked list"
        ],
        "Operating Systems": [
            "process", "thread", "deadlock",
            "scheduling", "memory management"
        ],
        "Database": [
            "database", "sql", "normalization",
            "transaction", "query"
        ],
        "Artificial Intelligence": [
            "machine learning", "artificial intelligence",
            "neural network", "classification",
            "clustering"
        ]
    }

    for category, keywords in topic_keywords.items():
        if any(keyword in lower_text for keyword in keywords):
            topic = category
            break

    # -----------------------------
    # 4. Extract key concepts
    # -----------------------------
    key_concepts = []

    for keyword in [
        "cpu",
        "cache",
        "memory",
        "processor",
        "stack",
        "queue",
        "tree",
        "graph",
        "database",
        "sql",
        "machine learning",
        "neural network"
    ]:
        if re.search(r"\b" + re.escape(keyword) + r"\b", lower_text):
            key_concepts.append(keyword)

    return {
        "topic": topic,
        "question_type": question_type,
        "difficulty": difficulty,
        "key_concepts": key_concepts
    }