import pandas as pd


# =========================
# STEP 1: IDENTIFY DELIVERABLES
# =========================
def extract_deliverables(df):

    df = df.copy()

    # Ensure required columns exist
    if "Activity Name" not in df.columns:
        raise ValueError("Missing Activity Name column")
    if "Finish" not in df.columns:
        raise ValueError("Missing Finish column")

    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # -------------------------
    # RULES TO IDENTIFY DELIVERABLES
    # -------------------------
    keywords = [
        "design", "report", "submission", "pack",
        "drawing", "manual", "model", "approval",
        "freeze", "register", "specification", "plan"
    ]

    def is_deliverable(name):
        if pd.isna(name):
            return False
        name_lower = name.lower()

        # exclude obvious activities
        exclude = [
            "mobilisation", "review", "workshop",
            "procurement", "installation", "lead",
            "governance", "construction"
        ]

        if any(x in name_lower for x in exclude):
            return False

        return any(k in name_lower for k in keywords)


    df = df[df["Activity Name"].apply(is_deliverable)].copy()

    # Rename into deliverable name
    df = df.rename(columns={"Activity Name": "Deliverable"})

    # Keep latest finish per deliverable group
    df = df.groupby("Deliverable", as_index=False)["Finish"].max()

    return df


# =========================
# STEP 2: COMPARE CL31 vs CL32
# =========================
def compare_deliverables(df31, df32):

    df31 = extract_deliverables(df31)
    df32 = extract_deliverables(df32)

    df31 = df31.rename(columns={"Finish": "CL31 Finish"})
    df32 = df32.rename(columns={"Finish": "CL32 Finish"})

    df = pd.merge(df31, df32, on="Deliverable", how="outer")

    # Delta
    df["Delta (Days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days


    # =========================
    # CHANGE TYPE LOGIC
    # =========================
    def change(row):
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


    df["Change Type"] = df.apply(change, axis=1)


    # =========================
    # COMMENTS
    # =========================
    def comment(row):
        if row["Change Type"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Change Type"] == "AHEAD":
            return "Pulled earlier, programme improvement"
        if row["Change Type"] == "UNCHANGED":
            return "Stable"
        if row["Change Type"] == "NEW":
            return "Added scope in CL32"
        if row["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        return "Check data"


    df["Status / Comment"] = df.apply(comment, axis=1)

    # Final format
    return df[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]