import numpy as np

def classify_float(df):

    if "Float" not in df.columns:
        df["Float"] = np.random.randint(0, 20, len(df))

    def status(f):
        if f <= 0:
            return "Critical"
        elif f <= 5:
            return "Near Critical"
        else:
            return "Non Critical"

    df["Status"] = df["Float"].apply(status)

    return df