def clean(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df