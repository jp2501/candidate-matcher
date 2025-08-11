import numpy as np
import pandas as pd

def cosine_similarity(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) or 1e-8
    return float(np.dot(a, b) / denom)

def to_table_rows(results):
    # minimal dataframe for display
    rows = [{"Name": r["name"], "Score": round(r["score"], 4), "Summary": r.get("summary", "")} for r in results]
    return pd.DataFrame(rows)
