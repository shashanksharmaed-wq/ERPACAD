"""
ERPACAD – Annual Academic Planning Engine
PERIOD-BASED | CBSE-ALIGNED | SAFE

Core principles:
- Principal sets ONLY total working days per class
- Engine plans in PERIODS, not days
- Revision, assessment, exams, remediation are mandatory
- Chapters cannot be rushed
"""

# =====================================================
# ACADEMIC CONFIGURATION (CBSE REALISTIC)
# =====================================================

PERIODS_PER_DAY = 8

CBSE_BLOCKS = {
    "teaching": 0.65,
    "revision": 0.10,
    "assessment": 0.10,
    "exams": 0.10,
    "buffer": 0.05
}

# Weekly subject frequency (typical CBSE middle school)
WEEKLY_PERIODS = {
    "Science": 5,
    "Mathematics": 5,
    "English": 5,
    "Social Science": 4,
    "Hindi": 4,
    "Language": 4,
    "Computer": 2,
    "GK": 2,
    "EVS": 5
}

# Base chapter load by class band
BASE_CHAPTER_PERIODS = {
    "primary": 6,     # Class 1–5
    "middle": 10,     # Class 6–8
    "secondary": 14  # Class 9–10
}

# Mandatory integrations per chapter
INTEGRATION_PERIODS = 3   # play + art/subject + language


# =====================================================
# INTERNAL HELPERS (TYPE SAFE)
# =====================================================

def normalize_grade(grade):
    """Ensures grade is always int."""
    try:
        return int(grade)
    except Exception:
        raise ValueError(f"Invalid grade value: {grade}")


def get_class_band(grade):
    """Returns academic band based on grade."""
    grade = normalize_grade(grade)

    if grade <= 5:
        return "primary"
    elif grade <= 8:
        return "middle"
    return "secondary"


def subject_key(subject: str) -> str:
    """Maps subject name to weekly period configuration."""
    subject_lower = subject.lower()

    for key in WEEKLY_PERIODS:
        if key.lower() in subject_lower:
            return key

    return "Language"


def calculate_chapter_periods(grade, subject, lo_count):
    """
    Calculates minimum required TEACHING periods for a chapter.
    Prevents unrealistic compression.
    """
    grade = normalize_grade(grade)
    band = get_class_band(grade)

    base = BASE_CHAPTER_PERIODS[band]

    # Learning outcome influence (soft cap)
    lo_factor = min(max(lo_count, 1), 5)

    required = base + lo_factor + INTEGRATION_PERIODS

    # Absolute academic safety floors
    if band == "middle" and required < 10:
        required = 10
    if band == "secondary" and required < 14:
        required = 14

    return required


# =====================================================
# MAIN ENGINE (PUBLIC FUNCTION)
# =====================================================

def generate_annual_plan(df, grade, subject, total_working_days):
    """
    Generates a CBSE-aligned annual plan for ONE class + ONE subject.

    Input:
    - grade (str/int)
    - subject (str)
    - total_working_days (int)

    Output:
    - Period-based academic plan
    """

    # -----------------------------
    # NORMALIZE INPUTS
    # -----------------------------
    grade = normalize_grade(grade)
    total_working_days = int(total_working_days)

    # -----------------------------
    # TOTAL PERIODS
    # -----------------------------
    total_periods = total_working_days * PERIODS_PER_DAY

    teaching_periods = int(total_periods * CBSE_BLOCKS["teaching"])

    # -----------------------------
    # WEEKLY SUBJECT FREQUENCY
    # -----------------------------
    subject_type = subject_key(subject)
    weekly_periods = WEEKLY_PERIODS.get(subject_type, 4)

    # -----------------------------
    # FILTER CHAPTER DATA
    # -----------------------------
    subject_df = df[
        (df["grade"] == grade) &
        (df["subject"] == subject)
    ]

    chapters = []
    total_required_periods = 0

    for chapter, group in subject_df.groupby("chapter"):
        lo_count = group["learning_outcome"].nunique()

        required_periods = calculate_chapter_periods(
            grade=grade,
            subject=subject,
            lo_count=lo_count
        )

        total_required_periods += required_periods

        chapters.append({
            "chapter": chapter,
            "required_periods": required_periods
        })

    # -----------------------------
    # NORMALIZE IF OVERFLOW
    # -----------------------------
    if total_required_periods > teaching_periods and total_required_periods > 0:
        scale = teaching_periods / total_required_periods

        band = get_class_band(grade)
        min_floor = BASE_CHAPTER_PERIODS[band]

        for ch in chapters:
            ch["required_periods"] = max(
                int(ch["required_periods"] * scale),
                min_floor
            )

    # -----------------------------
    # CALCULATE APPROX WEEKS
    # -----------------------------
    for ch in chapters:
        ch["approx_weeks"] = round(
            ch["required_periods"] / weekly_periods,
            1
        )
        ch["status"] = "Planned"

    # -----------------------------
    # FINAL PLAN OBJECT
    # -----------------------------
    return {
        "grade": grade,
        "subject": subject,
        "total_working_days": total_working_days,
        "periods_per_day": PERIODS_PER_DAY,
        "total_periods": total_periods,
        "teaching_periods": teaching_periods,
        "weekly_periods": weekly_periods,
        "chapters": chapters,
        "cbse_blocks": {
            "revision_periods": int(total_periods * CBSE_BLOCKS["revision"]),
            "assessment_periods": int(total_periods * CBSE_BLOCKS["assessment"]),
            "exam_periods": int(total_periods * CBSE_BLOCKS["exams"]),
            "buffer_periods": int(total_periods * CBSE_BLOCKS["buffer"])
        }
    }
