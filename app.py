# app.py (relevant bits)
import streamlit as st
from components.sidebar import render_top_nav
from backend.main import run_create_match_ui
from views.dashboard import render as render_dashboard
from views.results import render as render_results
from views.settings import render as render_settings

st.set_page_config(page_title="Candidate Matcher", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
  section[data-testid="stSidebar"]{display:none!important;}
  div[data-testid="stSidebarNav"]{display:none!important;}
  div.block-container{max-width:100%; padding-top:2.25rem;}
</style>
""", unsafe_allow_html=True)

# keep once
if "page" not in st.session_state:
    st.session_state.page = "Create Match"

# read current selection (keyed menu keeps it across reruns)
selected = render_top_nav(default=st.session_state.page)

# update the session only if it changed (no extra rerun needed)
if selected != st.session_state.page:
    st.session_state.page = selected

# router uses the current selection
if st.session_state.page == "Dashboard":
    render_dashboard()
elif st.session_state.page == "Create Match":
    run_create_match_ui()
elif st.session_state.page == "Results":
    render_results()
elif st.session_state.page == "Settings":
    render_settings()
