from math import floor

def generate_annual_plan(df, grade, subject, total_days):
    chapters = df[
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    groups = chapters.groupby("chapter")
    weights = []

    for chapter, g in groups:
        lo_count = len(g["learning_outcome"].dropna())
        weights.append({
            "chapter": chapter,
            "lo_count": lo_count,
            "days": max(1, lo_count)
        })

    total_weight = sum(w["days"] for w in weights)

    for w in weights:
        w["suggested_days"] = max(
            1, floor((w["days"] / total_weight) * total_days)
        )

    allocated = sum(w["suggested_days"] for w in weights)
    diff = total_days - allocated
    i = 0

    while diff != 0:
        weights[i % len(weights)]["suggested_days"] += 1 if diff > 0 else -1
        diff += -1 if diff > 0 else 1
        i += 1

    return weights
