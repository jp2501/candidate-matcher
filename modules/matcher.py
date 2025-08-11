from typing import List, Tuple
from modules.embedder import get_embedding
from modules.resume_parser import parse_resume
from modules.utils import cosine_similarity
from modules.summarizer import generate_summary

def process_resumes(
    resumes: List[Tuple[str, bytes]],
    role_type: str,
    job_summary: str,
    enable_ai_summary: bool = True,
):
    job_description = f"Role: {role_type}\n{job_summary}".strip()
    jd_embedding = get_embedding(job_description)

    results = []
    for filename, blob in resumes:
        parsed_text, name = parse_resume(filename, blob)
        res_emb = get_embedding(parsed_text)

        score = cosine_similarity(jd_embedding, res_emb)

        summary = ""
        if enable_ai_summary:
            try:
                summary = generate_summary(role_type, job_summary, parsed_text)
            except Exception as e:
                summary = f"(Summary unavailable: {e})"

        results.append(
            {"name": name, "score": round(score, 4), "summary": summary}
        )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
