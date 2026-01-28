import pandas as pd
import math

# ---------------- CBSE GUIDELINES ----------------
TOTAL_WEEKS = 30  # minimum CBSE instructional weeks

WEEKLY_PERIODS = {
    "math": 7,
    "mathematics": 7,
    "science": 6,
    "evs": 5,
    "english": 7,
    "hindi": 7,
    "social science": 6,
    "sst": 6,
}

# ---------------- UTILITIES ----------------
def normalize_columns(df):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def detect_column(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k in col:
                return col
    raise ValueError(f"Required column not found: {keywords}")


def get_weekly_periods(subject):
    s = subject.lower()
    for key, val in WEEKLY_PERIODS.items():
        if key in s:
            return val
    return 5  # safe default


# ---------------- MAIN ENGINE ----------------
def generate_annual_plan(df, selected_class, selected_subject, academic_days):

    df = normalize_columns(df)

    class_col = detect_column(df, ["class", "grade", "std"])
    subject_col = detect_column(df, ["subject"])
    chapter_col = detect_column(df, ["chapter"])
    lo_col = detect_column(df, ["learning_outcome", "lo"])

    # Filter subject + class
    subject_df = df[
        (df[class_col] == selected_class) &
        (df[subject_col].str.lower() == selected_subject.lower())
    ]

    if subject_df.empty:
        return {"chapters": [], "message": "No syllabus data found."}

    weekly_periods = get_weekly_periods(selected_subject)
    total_periods = TOTAL_WEEKS * weekly_periods

    chapter_groups = subject_df.groupby(chapter_col)
    total_los = chapter_groups[lo_col].nunique().sum()

    chapters = []

    for chapter, group in chapter_groups:
        lo_count = group[lo_col].nunique()

        # Proportional allocation (CBSE safe)
        periods = max(
            2,
            math.ceil((lo_count / total_los) * total_periods)
        )

        chapters.append({
            "Chapter": chapter,
            "Learning Outcomes": lo_count,
            "Total Periods": periods,
            "Approx Weeks": round(periods / weekly_periods, 1)
        })

    return {
        "weekly_periods": weekly_periods,
        "total_periods": total_periods,
        "chapters": chapters
    }
