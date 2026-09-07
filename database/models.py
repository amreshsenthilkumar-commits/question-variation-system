from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database.connection import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    seed_question = Column(
        Text,
        nullable=False
    )

    topic = Column(
        String(100),
        nullable=False
    )

    question_type = Column(
        String(100),
        nullable=False
    )

    difficulty = Column(
        String(50),
        nullable=False
    )

    key_concepts = Column(
        Text,
        nullable=True
    )

    requested_variations = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    variations = relationship(
        "Variation",
        back_populates="question",
        cascade="all, delete-orphan"
    )


class Variation(Base):
    __tablename__ = "variations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    variation_id = Column(
        Integer,
        nullable=False
    )

    variation_question = Column(
        Text,
        nullable=False
    )

    changed_aspect = Column(
        Text,
        nullable=True
    )

    learning_objective = Column(
        Text,
        nullable=True
    )

    cognitive_operation = Column(
        String(100),
        nullable=True
    )

    difficulty = Column(
        String(50),
        nullable=True
    )

    similarity_score = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    question = relationship(
        "Question",
        back_populates="variations"
    )