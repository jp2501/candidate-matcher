# components/sidebar.py
import streamlit as st
from streamlit_option_menu import option_menu

def render_top_nav(default="Create Match"):
        # Robust full-width navbar (no :has selector)
    st.markdown(
        """
        <style>
          /* Make the main container full width */
          div.block-container { max-width: 100% !important; }
          /* Wrap a class around the menu and force full width */
          .topnav-wrap nav { width: 100% !important; }
          .topnav-wrap nav ul {
              width: 100% !important;
              display: flex !important;
              flex-wrap: wrap !important;
              justify-content: space-between !important;
              gap: .5rem;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
    pages = ["Dashboard", "Create Match", "Results", "Settings"]
    try:
        idx = pages.index(default)
    except ValueError:
        idx = 1  # fallback to "Create Match"

    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=["speedometer2", "plus-circle", "list-check", "gear"],
        orientation="horizontal",
        default_index=idx,
        key="topnav",  # <-- persistent key fixes double-click
        styles={
            "container": {"padding": "0", "background": "transparent", "width": "100%"},
            "nav": {"justify-content": "space-between"},
            "nav-link": {"padding": "8px 16px", "border-radius": "8px"},
            "nav-link-selected": {"background-color": "#1f6feb"},
        },
    )
    st.markdown("---")
    return selected
