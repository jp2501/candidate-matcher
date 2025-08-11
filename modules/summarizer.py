# modules/summarizer.py
import os
import re
import torch
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

# Primary model requested (Gemma by default)
PRIMARY_MODEL = os.getenv("SUMMARIZER_MODEL", "google/gemma-2b-it")
# Fallback that runs almost anywhere
FALLBACK_MODEL = "google/flan-t5-base"

def _format_prompt(role: str, jd: str, resume_text: str) -> str:
    return (
        "You are an expert technical recruiter. "
        "Given a job description and a candidate resume, write a 2-3 sentence, specific summary of fit. "
        "Focus on skills, experience, and keywords; avoid generic praise.\n\n"
        f"Job: {role}\n"
        f"Description:\n{jd}\n\n"
        f"Resume:\n{(resume_text or '')[:4000]}\n\n"
        "Summary:"
    )

def _trim_to_2_3_sentences(text: str) -> str:
    text = (text or "").strip()
    # Drop any leading "Summary:" echoes or boilerplate
    text = re.sub(r"^\s*summary\s*:?\s*", "", text, flags=re.IGNORECASE).strip()
    # Split into sentences and keep up to 3
    parts = re.split(r"(?<=[.!?])\s+", text)
    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        return ""
    # Keep max 3 sentences
    trimmed = " ".join(parts[:3])
    return trimmed

@lru_cache(maxsize=1)
def _load_model_pair():
    model_name = PRIMARY_MODEL
    try:
        tok = AutoTokenizer.from_pretrained(model_name)
        # Gemma is a causal LM
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
        )
        return tok, model, model_name
    except Exception:
        # Fallback: T5 must use Seq2Seq
        tok = AutoTokenizer.from_pretrained(FALLBACK_MODEL)
        model = AutoModelForSeq2SeqLM.from_pretrained(
            FALLBACK_MODEL,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        )
        if torch.cuda.is_available():
            model = model.cuda()
        return tok, model, FALLBACK_MODEL

def generate_summary(role: str, jd: str, resume_text: str) -> str:
    tok, model, used = _load_model_pair()
    prompt = _format_prompt(role, jd, resume_text)

    # Tokenize safely
    inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=4096)
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}

    # FLAN-T5 (seq2seq) branch
    if "flan-t5" in used.lower():
        out = model.generate(
            **inputs,
            max_new_tokens=140,
            num_beams=4,                 # higher quality, deterministic
            length_penalty=1.0,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )
        text = tok.decode(out[0], skip_special_tokens=True)
        return _trim_to_2_3_sentences(text)

    # Gemma / causal LM branch
    out = model.generate(
        **inputs,
        max_new_tokens=140,
        do_sample=True,
        temperature=0.4,
        top_p=0.95,
        pad_token_id=getattr(tok, "eos_token_id", None),
    )
    text = tok.decode(out[0], skip_special_tokens=True)
    # If the model echoed the prompt, keep only text after the last "Summary:"
    text = text.split("Summary:")[-1].strip() or text.strip()
    return _trim_to_2_3_sentences(text)
