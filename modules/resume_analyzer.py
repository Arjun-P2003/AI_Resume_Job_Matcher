
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """
    Clean resume or job description text.
    """

    text = text.lower()
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_similarity(resume_text, job_description):
    """
    Calculate similarity between a resume
    and a job description using TF-IDF
    and cosine similarity.
    """

    if not resume_text.strip() or not job_description.strip():
        return 0.0

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(similarity * 100, 2)

    except ValueError:
        return 0.0
