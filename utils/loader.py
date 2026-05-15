import pandas as pd

def load_programme_data():
    """
    Loads CL31 and CL32 programme data
    """

    cl31_path = "data/CL31.xlsx"
    cl32_path = "data/CL32.xlsx"

    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    # -----------------------------
    # STANDARDISE COLUMN NAMES
    # -----------------------------

    def clean_columns(df):
        df.columns = [c.strip() for c in df.columns]

        rename_map = {
            "Total Float": "Float Change",
            "Float": "Float Change",
            "BL1 Finish": "CL31 Finish",
            "CL32 Finish": "CL32 Finish",
        }

        df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

        return df

    cl31 = clean_columns(cl31)
    cl32 = clean_columns(cl32)

    return cl31, cl32