import streamlit as st

def render():
    # Ensure defaults exist even if user lands here first
    s = st.session_state.setdefault(
        "settings",
        {"show_top_k": 10, "enable_ai_summary": True, "similarity_threshold": 0.0},
    )

    st.title("Settings")
    s["show_top_k"] = st.slider("Show Top K Candidates", 1, 50, s.get("show_top_k", 10))
    s["similarity_threshold"] = st.slider(
        "Similarity Threshold", 0.0, 1.0, float(s.get("similarity_threshold", 0.0)), 0.01
    )
    s["enable_ai_summary"] = st.toggle(
        "Generate AI Summaries (Gemma 2B IT)", s.get("enable_ai_summary", True)
    )
    st.session_state.settings = s
    st.success("Settings saved for this session.")
