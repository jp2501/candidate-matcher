# FastAPI backend (optional) + Streamlit "Create Match" page UI
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
# shared logic
from modules.matcher import process_resumes
from modules.utils import to_table_rows

import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# --- Optional FastAPI service (you can ignore if not needed) ---
app = FastAPI(title="Candidate Matcher Backend")

class MatchItem(BaseModel):
    filename: str
    content_b64: str  # base64 encoded bytes

class MatchRequest(BaseModel):
    role_type: str
    job_summary: str
    resumes: List[MatchItem]
    enable_ai_summary: bool = True
    top_k: int = 10

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match")
def match(req: MatchRequest):
    # In a real deployment, decode base64 and pass raw bytes along with filename
    import base64
    inputs = [(r.filename, base64.b64decode(r.content_b64)) for r in req.resumes]
    results = process_resumes(
        inputs,
        role_type=req.role_type,
        job_summary=req.job_summary,
        enable_ai_summary=req.enable_ai_summary,
    )
    return {"results": results[: req.top_k]}

# --- Streamlit UI for "Create Match" ---
def run_create_match_ui():
    import streamlit as st

    st.title("Create Match")
    st.caption("Upload resumes, paste a role, and get ranked candidates.")

    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            role_type = st.text_input("Role Type", placeholder="e.g., Backend Engineer")
            department = st.text_input("Department (optional)", placeholder="e.g., Platform")
            exp = st.selectbox("Experience Level", ["Any", "Intern", "Junior", "Mid", "Senior", "Lead"], index=0)
            location = st.text_input("Location (optional)", placeholder="e.g., Remote / NYC / Bangalore")
        with col2:
            jd = st.text_area(
                "Job Description",
                height=240,
                placeholder="Paste responsibilities + requirements. The more detail, the better.",
            )

    st.markdown("### Resumes")
    uploads = st.file_uploader(
        "Upload multiple resumes (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True
    )

    st.markdown("#### Tips")
    st.write("- Provide detailed JD for best results.\n- PDF/DOCX/TXT supported.\n- Turn on AI summary in Settings.")

    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        submit = st.button("Submit", type="primary", use_container_width=True)
    with c2:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state.results = []
        st.success("Cleared previous results.")

    if submit:
        if not role_type and not jd:
            st.error("Please provide at least Role Type or Job Description.")
            return
        if not uploads:
            st.error("Please upload at least one resume.")
            return

        # Compose JD block (mirrors your React structure)
        job_summary_parts = []
        if department: job_summary_parts.append(f"Department: {department}")
        if exp and exp != "Any": job_summary_parts.append(f"Experience: {exp}")
        if location: job_summary_parts.append(f"Location: {location}")
        prefix = "\n".join(job_summary_parts)
        job_summary = (prefix + ("\n" if prefix and jd else "") + jd).strip()

        # Convert UploadedFile objects into (filename, bytes)
        resume_blobs = [(f.name, f.read()) for f in uploads]

        with st.spinner("Matching… this may take a moment if AI summaries are enabled."):
            results = process_resumes(
                resume_blobs,
                role_type=role_type,
                job_summary=job_summary,
                enable_ai_summary=st.session_state.settings.get("enable_ai_summary", True),
            )

        # Threshold + top_k filtering
        threshold = st.session_state.settings.get("similarity_threshold", 0.0) or 0.0
        results = [r for r in results if r["score"] >= threshold]
        top_k = st.session_state.settings.get("show_top_k", 10) or 10
        st.session_state.results = results[:top_k]

        st.success(f"Done! Found {len(st.session_state.results)} candidates.")
        
        # Quick peek table (full summaries; no truncation, no clicking)
        if st.session_state.results:
            df = to_table_rows(st.session_state.results)  # -> columns: Name, Score, Summary
            if "Score" in df.columns:
                df["Score"] = df["Score"].map(lambda x: f"{float(x):.4f}")

            FULL_WRAP_CSS = """
            <style>
            table.fullwrap { width:100%; border-collapse:collapse; table-layout:fixed; }
            .fullwrap th, .fullwrap td { border:1px solid #eee; padding:10px; vertical-align:top; }
            .fullwrap th { background:#f8f9fb; text-align:left; }
            /* allow long text to wrap and rows to grow */
            .fullwrap td { white-space:normal; word-wrap:break-word; word-break:break-word; }
            /* make Summary column wide */
            .fullwrap th:nth-child(3), .fullwrap td:nth-child(3) { width:60%; }
            </style>
            """
            st.markdown(FULL_WRAP_CSS, unsafe_allow_html=True)
            st.markdown(df.to_html(classes="fullwrap", index=False, escape=False), unsafe_allow_html=True)