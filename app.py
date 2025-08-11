import streamlit as st

# Page config + hide Streamlit's sidebar
st.set_page_config(page_title="Candidate Matcher", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
  section[data-testid="stSidebar"]{display:none!important;}
  div[data-testid="stSidebarNav"]{display:none!important;}
  /* push content (incl. navbar) down a bit so the highlight isn't clipped */
  div.block-container{max-width:100%; padding-top:2.25rem;}
</style>
""", unsafe_allow_html=True)

# --- Session defaults (MUST be set before importing views/UI renderers) ---
st.session_state.setdefault("page", "Create Match")
st.session_state.setdefault("results", [])
st.session_state.setdefault(
    "settings",
    {
        "show_top_k": 10,
        "enable_ai_summary": True,
        "similarity_threshold": 0.0,
    },
)

# Now import UI pieces (safe after session_state init)
from components.sidebar import render_top_nav
from backend.main import run_create_match_ui
from views.dashboard import render as render_dashboard
from views.results import render as render_results
from views.settings import render as render_settings

# Horizontal navbar (give it a stable key inside the component)
selected = render_top_nav(default=st.session_state.page)

# Update router state only if it changed
if selected != st.session_state.page:
    st.session_state.page = selected

# Route
if st.session_state.page == "Dashboard":
    render_dashboard()
elif st.session_state.page == "Create Match":
    run_create_match_ui()
elif st.session_state.page == "Results":
    render_results()
elif st.session_state.page == "Settings":
    render_settings()
else:
    run_create_match_ui()
