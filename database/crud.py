from sqlalchemy.orm import Session

from database.models import Question, Variation


def create_question(
    db: Session,
    seed_question: str,
    analysis: dict,
    requested_variations: int
):
    """
    Save the seed question and its analysis
    into the questions table.
    """

    question = Question(
        seed_question=seed_question,

        topic=analysis.get(
            "topic",
            "General"
        ),

        question_type=analysis.get(
            "question_type",
            "General"
        ),

        difficulty=analysis.get(
            "difficulty",
            "Medium"
        ),

        key_concepts=", ".join(
            analysis.get(
                "key_concepts",
                []
            )
        ),

        requested_variations=requested_variations
    )

    db.add(question)

    db.commit()

    db.refresh(question)

    return question


def create_variation(
    db: Session,
    question_id: int,
    variation: dict
):
    """
    Save one generated variation
    into the variations table.
    """

    new_variation = Variation(

        question_id=question_id,

        variation_id=variation.get(
            "variation_id"
        ),

        variation_question=variation.get(
            "question",
            ""
        ),

        changed_aspect=variation.get(
            "changed_aspect"
        ),

        learning_objective=variation.get(
            "learning_objective"
        ),

        cognitive_operation=variation.get(
            "cognitive_operation"
        ),

        difficulty=variation.get(
            "difficulty"
        ),

        similarity_score=variation.get(
            "similarity_score"
        )
    )

    db.add(new_variation)

    db.commit()

    db.refresh(new_variation)

    return new_variation