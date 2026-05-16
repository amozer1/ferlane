import pandas as pd


def build_comparison(df31, df32):
    key_col = "Activity ID"
    finish_col = "Finish"

    # Keep only relevant columns
    df31 = df31[[key_col, finish_col]].copy()
    df32 = df32[[key_col, finish_col]].copy()

    df31 = df31.rename(columns={finish_col: "CL31 Finish"})
    df32 = df32.rename(columns={finish_col: "CL32 Finish"})

    # Merge full outer (important for NEW + REMOVED detection)
    df = pd.merge(df31, df32, on=key_col, how="outer")

    # Convert dates
    df["CL31 Finish"] = pd.to_datetime(df["CL31 Finish"], errors="coerce")
    df["CL32 Finish"] = pd.to_datetime(df["CL32 Finish"], errors="coerce")

    # Delta
    df["Delta (Days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days


    # =========================
    # Change classification
    # =========================
    def classify(row):
        a = row["CL31 Finish"]
        b = row["CL32 Finish"]

        if pd.isna(a) and pd.notna(b):
            return "NEW"
        if pd.notna(a) and pd.isna(b):
            return "REMOVED"
        if pd.notna(a) and pd.notna(b):
            if row["Delta (Days)"] == 0:
                return "UNCHANGED"
            elif row["Delta (Days)"] > 0:
                return "DELAYED"
            else:
                return "AHEAD"
        return "UNKNOWN"


    df["Change Type"] = df.apply(classify, axis=1)

    # =========================
    # Comments engine
    # =========================
    def comment(row):
        if row["Change Type"] == "DELAYED":
            return f"Shifted later by {row['Delta (Days)']} days, coordination required"
        elif row["Change Type"] == "AHEAD":
            return f"Pulled earlier by {abs(row['Delta (Days)'])} days"
        elif row["Change Type"] == "UNCHANGED":
            return "Stable"
        elif row["Change Type"] == "NEW":
            return "Added scope in CL32"
        elif row["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        return "Check data"


    df["Status / Comment"] = df.apply(comment, axis=1)

    # Final output
    output = df[[
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    return output