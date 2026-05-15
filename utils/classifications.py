import numpy as np

def classify_status(df):
    """
    Assigns NEC programme status based on float and variance rules
    """

    def get_status(row):
        float_val = row.get("Float", 0)
        variance = row.get("Variance - BL1 Finish Date", 0)

        # 🔴 Critical
        if float_val <= 0 or variance <= -14:
            return "Critical"

        # 🟡 Near Critical
        elif float_val <= 10 or (-13 <= variance <= -5):
            return "Near Critical"

        # 🟢 On Track
        elif float_val > 10 and variance > -5:
            return "On Track"

        # fallback
        return "On Track"

    df["Status"] = df.apply(get_status, axis=1)

    return df


def classify_float(df):
    """
    Optional alias so your old imports don't break immediately
    """
    return classify_status(df)