import pandas as pd

def load_schedule(cl31_path, cl32_path):
    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    return cl31, cl32


def extract_deliverables(df):
    """
    Pull ONLY top-level deliverables (no indentation children)
    Assumption: Deliverables are summary rows with missing Activity ID OR no 'FER-' codes
    """

    df = df.copy()

    # Clean column names just in case
    df.columns = [c.strip() for c in df.columns]

    # Identify deliverable rows (summary level)
    deliverables = df[
        df["Activity Name"].notna() &
        ~df["Activity ID"].astype(str).str.contains("FER-", na=False)
    ].copy()

    return deliverables