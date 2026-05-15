import pandas as pd

def clean_programme(df):
    """
    Standardises column names for CL31/CL32 consistency
    """

    df.columns = df.columns.str.strip()

    # Ensure required columns exist safely
    required = [
        "Activity ID",
        "Activity Name",
        "Start",
        "Finish"
    ]

    for col in required:
        if col not in df.columns:
            df[col] = None

    return df