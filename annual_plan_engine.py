import pandas as pd
import math

TOTAL_WEEKS = 30

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

def normalize_columns(df):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def detect_column(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k in col:
                return col
    raise ValueError(f"Missing column: {keywords}")

def get_weekly_periods(subject):
    s = subject.lower()
    for key, val in WEEKLY_PERIODS.items():
        if key in s:
            return val
    return 5

def generate_annual_plan(df, grade, subject, academic_days):
    df = normalize_columns(df)

    class_col = detect_column(df, ["class", "grade", "std"])
    subject_col = detect_column(df, ["subject"])
    chapter_col = detect_column(df, ["chapter"])
    lo_col = detect_column(df, ["learning_outcome", "lo"])

    sdf = df[
        (df[class_col] == grade) &
        (df[subject_col].str.lower() == subject.lower())
    ]

    if sdf.empty:
        return {"chapters": []}

    weekly = get_weekly_periods(subject)
    total_periods = TOTAL_WEEKS * weekly

    groups = sdf.groupby(chapter_col)
    total_los = groups[lo_col].nunique().sum()

    chapters = []
    for ch, g in groups:
        lo_count = g[lo_col].nunique()
        periods = max(2, math.ceil((lo_count / total_los) * total_periods))

        chapters.append({
            "Chapter": ch,
            "Learning Outcomes": lo_count,
            "Total Periods": periods
        })

    return {
        "weekly_periods": weekly,
        "total_periods": total_periods,
        "chapters": chapters
    }
