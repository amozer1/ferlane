import pandas as pd


def classify_activity(row):

    # ============================================
    # NEW ACTIVITY
    # ============================================

    if pd.isna(row["Finish_31"]):
        return "New Activity"

    # ============================================
    # REMOVED ACTIVITY
    # ============================================

    elif pd.isna(row["Finish_32"]):
        return "Removed"

    # ============================================
    # DELAYED
    # ============================================

    elif row["Delta Finish Days"] > 0:
        return "Delayed"

    # ============================================
    # ACCELERATED
    # ============================================

    elif row["Delta Finish Days"] < 0:
        return "Accelerated"

    # ============================================
    # ON TRACK
    # ============================================

    else:
        return "On Track"