from database.connection import SessionLocal
from database.crud import create_question, create_variation


analysis = {
    "topic": "Computer Architecture",
    "question_type": "Explanation",
    "difficulty": "Medium",
    "key_concepts": [
        "cpu",
        "cache"
    ]
}


db = SessionLocal()


try:

    question = create_question(
        db=db,
        seed_question=(
            "Explain how CPU cache improves "
            "processor performance."
        ),
        analysis=analysis,
        requested_variations=2
    )

    print(
        "Question saved successfully!"
    )

    print(
        "Question ID:",
        question.id
    )


    variation_data = {
        "variation_id": 1,
        "question": (
            "Explain how cache memory reduces "
            "the time required for CPU data access."
        ),
        "changed_aspect": "Data access scenario",
        "learning_objective": (
            "Explanation: Explain how CPU cache "
            "improves processor performance."
        ),
        "cognitive_operation": "Explanation",
        "difficulty": "Medium",
        "similarity_score": 0.349
    }


    variation = create_variation(
        db=db,
        question_id=question.id,
        variation=variation_data
    )


    print(
        "Variation saved successfully!"
    )

    print(
        "Variation ID:",
        variation.id
    )


finally:

    db.close()