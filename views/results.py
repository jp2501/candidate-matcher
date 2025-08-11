import io, csv
import streamlit as st
from modules.utils import to_table_rows

def render():
    st.title("Results")
    results = st.session_state.get("results", [])
    if not results:
        st.info("No results yet. Run a match from **Create Match**.")
        return

    df = to_table_rows(results)
    # Show full wrapped summaries (same HTML table trick)
    FULL_WRAP_CSS = """
    <style>
      table.fullwrap { width:100%; border-collapse:collapse; table-layout:fixed; }
      .fullwrap th, .fullwrap td { border:1px solid #eee; padding:10px; vertical-align:top; }
      .fullwrap th { background:#f8f9fb; text-align:left; }
      .fullwrap td { white-space:normal; word-wrap:break-word; word-break:break-word; }
      .fullwrap th:nth-child(3), .fullwrap td:nth-child(3) { width:60%; }
    </style>
    """
    if "Score" in df.columns: df["Score"] = df["Score"].map(lambda x: f"{float(x):.4f}")
    st.markdown(FULL_WRAP_CSS, unsafe_allow_html=True)
    st.markdown(df.to_html(classes="fullwrap", index=False, escape=False), unsafe_allow_html=True)

    # CSV download
    csv_io = io.StringIO()
    cw = csv.writer(csv_io)
    cw.writerow(["Name", "Score", "Summary"])
    for r in results:
        cw.writerow([r["name"], r["score"], r.get("summary","")])
    st.download_button("Download CSV", data=csv_io.getvalue().encode("utf-8"),
                       file_name="candidate_match_results.csv", mime="text/csv")
