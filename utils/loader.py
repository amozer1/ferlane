import pandas as pd

def build_card_one(cl31, cl32):

    table = pd.DataFrame()

    # Deliverable (assumes row alignment)
    if "Deliverable" in cl32.columns:
        table["Deliverable"] = cl32["Deliverable"]
    else:
        table["Deliverable"] = cl32.index

    # Dates
    table["CL31 Finish"] = pd.to_datetime(cl31["Finish"], errors="coerce").dt.strftime("%d-%b-%y")
    table["CL32 Finish"] = pd.to_datetime(cl32["Finish"], errors="coerce").dt.strftime("%d-%b-%y")

    # Δ Finish (Days)
    table["Δ Finish (Days)"] = (
        pd.to_datetime(cl32["Finish"], errors="coerce")
        - pd.to_datetime(cl31["Finish"], errors="coerce")
    ).dt.days.fillna(0).astype(int)

    # Float Change
    if "Float" in cl32.columns:
        table["Float Change"] = cl32["Float"].fillna(0).astype(int)
    else:
        table["Float Change"] = 0

    # Status
    def status(f):
        if f <= 0:
            return "🔴 Delayed"
        elif f <= 5:
            return "🟡 At Risk"
        else:
            return "🟢 On Track"

    table["Status"] = table["Float Change"].apply(status)

    return table