import pandas as pd


def identify_deliverables(df):
    """
    Deliverables are extracted dynamically
    from Activity Name rows that contain:
    - finish dates
    - baseline finish dates
    - are not activity IDs
    """

    deliverables = df.copy()

    deliverables = deliverables[
        deliverables["Activity Name"].notna()
    ]

    deliverables = deliverables[
        deliverables["Activity Name"] != ""
    ]

    deliverables = deliverables[
        deliverables["Finish"].notna()
    ]

    deliverables = deliverables[
        deliverables["BL1 Finish"].notna()
    ]

    # remove ID-like rows
    deliverables = deliverables[
        ~deliverables["Activity Name"].str.match(
            r"^[A-Z0-9\-]+$",
            na=False
        )
    ]

    deliverables = deliverables.drop_duplicates(
        subset=["Activity Name"]
    )

    return deliverables


def determine_status(float_value):
    if pd.isna(float_value):
        return "⚪ Unknown"

    if float_value < 0:
        return "🔴 Critical"

    if float_value <= 10:
        return "🟡 At Risk"

    return "🟢 On Track"


def compare_deliverables(cl31, cl32):

    cl31 = identify_deliverables(cl31)
    cl32 = identify_deliverables(cl32)

    cl31 = cl31.rename(columns={
        "Finish": "CL31 Finish",
        "Total Float": "CL31 Float"
    })

    cl32 = cl32.rename(columns={
        "Finish": "CL32 Finish",
        "Total Float": "CL32 Float"
    })

    merged = pd.merge(
        cl31[
            [
                "Activity Name",
                "CL31 Finish",
                "CL31 Float"
            ]
        ],
        cl32[
            [
                "Activity Name",
                "CL32 Finish",
                "CL32 Float"
            ]
        ],
        on="Activity Name",
        how="inner"
    )

    merged["Δ Finish (Days)"] = (
        merged["CL32 Finish"] -
        merged["CL31 Finish"]
    ).dt.days

    merged["Float Change"] = (
        merged["CL32 Float"] -
        merged["CL31 Float"]
    )

    merged["Status"] = merged[
        "CL32 Float"
    ].apply(determine_status)

    merged = merged.rename(columns={
        "Activity Name": "Deliverable"
    })

    merged["CL31 Finish"] = merged[
        "CL31 Finish"
    ].dt.strftime("%d-%b-%y")

    merged["CL32 Finish"] = merged[
        "CL32 Finish"
    ].dt.strftime("%d-%b-%y")

    merged["Δ Finish (Days)"] = merged[
        "Δ Finish (Days)"
    ].apply(
        lambda x: f"{x:+}" if pd.notna(x) else ""
    )

    merged["Float Change"] = merged[
        "Float Change"
    ].apply(
        lambda x: f"{int(x):+}" if pd.notna(x) else ""
    )

    merged = merged.sort_values(
        by="Deliverable"
    )

    return merged[
        [
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Δ Finish (Days)",
            "Float Change",
            "Status"
        ]
    ]