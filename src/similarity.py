from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(resume_text, job_description):
    """
    Calculate semantic similarity between a resume
    and a job description using sentence embeddings.
    """

    model = load_model()

    embeddings = model.encode([
        resume_text,
        job_description
    ])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(similarity)