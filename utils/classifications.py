def classify_status(row):

    delta = row["Delta_Days"]
    float_change = row["Float_Change"]

    if delta >= 14 or float_change <= -10:
        return "Critical"

    elif 5 <= delta < 14:
        return "At Risk"

    elif delta <= 4 and float_change > -10:
        return "On Track"

    else:
        return "On Track"