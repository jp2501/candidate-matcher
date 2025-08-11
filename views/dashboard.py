import streamlit as st

def render():
    st.title("Dashboard")
    st.caption("Quick glance at your recent runs.")
    res = st.session_state.get("results", [])
    st.metric("Last Match Count", len(res))
    if res:
        best = res[0]
        st.success(f"Top candidate: **{best['name']}** (score {best['score']})")
        with st.expander("See all current results"):
            import pandas as pd
            st.dataframe(pd.DataFrame(res), use_container_width=True)
    else:
        st.info("No results yet. Head to **Create Match** to run your first match.")
