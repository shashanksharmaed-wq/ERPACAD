import pandas as pd
import math

# -----------------------------
# CBSE weekly period guidance
# -----------------------------
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

TOTAL_WEEKS = 30  # CBSE minimum instructional weeks


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def detect_chapter_column(df: pd.DataFrame) -> str:
    for col in df.columns:
        if "chapter" in col:
            return col
    raise ValueError("❌ No chapter column found in TSV")


def detect_subject_column(df: pd.DataFrame) -> str:
    for col in df.columns:
        if col in ["subject", "subjects"]:
            return col
    raise ValueError("❌ No subject column found in TSV")


def get_weekly_periods(subject: str) -> int:
    if not subject:
        return 5
    s = subject.lower()
    for key, value in WEEKLY_PERIODS.items():
        if key in s:
            return value
    return 5  # safe default


def generate_annual_plan(df, grade, subject, academic_days):
    df = normalize_columns(df)

    chapter_col = detect_chapter_column(df)
    subject_col = detect_subject_column(df)

    # Filter data
    subject_df = df[
        (df["class"] == grade) &
        (df[subject_col].str.lower() == subject.lower())
    ]

    if subject_df.empty:
        return {"chapters": [], "message": "No data found for this selection"}

    weekly_periods = get_weekly_periods(subject)
    total_periods = TOTAL_WEEKS * weekly_periods

    # Group by chapter
    chapter_groups = subject_df.groupby(chapter_col)

    chapters = []
    total_los = chapter_groups["learning_outcome"].nunique().sum()

    for chapter, group in chapter_groups:
        lo_count = group["learning_outcome"].nunique()

        # proportional allocation
        chapter_periods = max(
            2,
            math.ceil((lo_count / total_los) * total_periods)
        )

        chapters.append({
            "chapter": chapter,
            "learning_outcomes": lo_count,
            "periods": chapter_periods,
            "weeks": round(chapter_periods / weekly_periods, 1)
        })

    return {
        "weekly_periods": weekly_periods,
        "total_periods": total_periods,
        "chapters": chapters
    }
