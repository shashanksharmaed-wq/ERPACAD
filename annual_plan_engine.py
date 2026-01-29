import math

def generate_annual_plan(df, grade, subject, academic_days):
    subject_df = df[
        (df["class"] == grade) &
        (df["subject"].str.lower() == subject.lower())
    ]

    chapters = subject_df["chapter"].unique().tolist()
    total_chapters = len(chapters)

    days_per_chapter = max(3, academic_days // total_chapters)

    plan = []
    for ch in chapters:
        los = subject_df[subject_df["chapter"] == ch]["learning_outcome"].tolist()
        plan.append({
            "chapter": ch,
            "days": days_per_chapter,
            "los": los
        })

    return plan
