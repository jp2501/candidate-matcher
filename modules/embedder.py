from functools import lru_cache
from sentence_transformers import SentenceTransformer

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # fast, light, good enough

@lru_cache(maxsize=1)
def _load_model():
    return SentenceTransformer(EMBED_MODEL_NAME)

def get_embedding(text: str):
    model = _load_model()
    # sentence-transformers returns np.ndarray
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()
