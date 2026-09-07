from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SIMILARITY_THRESHOLD = 0.50


def calculate_similarity(seed_question: str, variation_question: str) -> float:
    """
    Calculate textual similarity between the seed question
    and a generated variation using TF-IDF and cosine similarity.
    """

    documents = [
        seed_question.strip().lower(),
        variation_question.strip().lower()
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(similarity), 3)


def is_too_similar(seed_question: str, variation_question: str) -> bool:
    """
    Return True if the variation is too similar to the seed question.
    """

    similarity = calculate_similarity(
        seed_question,
        variation_question
    )

    return similarity >= SIMILARITY_THRESHOLD