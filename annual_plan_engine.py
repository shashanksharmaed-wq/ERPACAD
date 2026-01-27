import pandas as pd
from math import floor

# ================= ANNUAL PLAN ENGINE =================

def generate_annual_plan(df, grade, subject, total_working_days):
    """
    Generates a chapter-wise annual plan based on learning outcome weight.
    Principal can adjust ONLY total_working_days.
    """

    chapters = df[
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    chapter_groups = chapters.groupby("chapter")

    chapter_weights = []
    for chapter, group in chapter_groups:
        lo_count = len(group["learning_outcomes"].dropna())
        chapter_weights.append({
            "chapter": chapter,
            "learning_outcomes": lo_count,
            "weight": max(lo_count, 1)
        })

    total_weight = sum(c["weight"] for c in chapter_weights)

    # Initial allocation
    for c in chapter_weights:
        c["suggested_days"] = max(
            1,
            floor((c["weight"] / total_weight) * total_working_days)
        )

    # Normalization to match total days
    allocated = sum(c["suggested_days"] for c in chapter_weights)
    diff = total_working_days - allocated

    i = 0
    while diff != 0:
        chapter_weights[i % len(chapter_weights)]["suggested_days"] += 1 if diff > 0 else -1
        diff += -1 if diff > 0 else 1
        i += 1

    return chapter_weights
