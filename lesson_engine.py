"""
ERPACAD – Lesson Execution Engine
PERIOD-BASED | ONE PERIOD AT A TIME | SAFE
"""

import os
from openai import OpenAI

# -------------------------------------------------
# PERIOD STRUCTURE (1 PERIOD = 40–45 MIN)
# -------------------------------------------------

PERIOD_STRUCTURE = [
    ("Engage", 5),
    ("Concept Build", 15),
    ("Guided Practice", 10),
    ("Integration / Activity", 10),
    ("Closure & Assessment", 5)
]

# -------------------------------------------------
# AI CLIENT (OPTIONAL)
# -------------------------------------------------

def get_ai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

# -------------------------------------------------
# TEACHING SCRIPT (ONE PERIOD ONLY)
# -------------------------------------------------

def generate_teaching_script(
    grade,
    subject,
    chapter,
    period_no,
    pedagogy,
    learning_outcomes,
    integration,
    language
):
    client = get_ai_client()

    # If AI unavailable, return structured fallback
    if not client:
        return (
            "Follow the lesson flow strictly.\n\n"
            "1. Engage students with prior knowledge questions.\n"
            "2. Introduce core concepts using examples.\n"
            "3. Conduct guided practice.\n"
            "4. Perform integration activity.\n"
            "5. Close with assessment and recap."
        )

    prompt = f"""
You are an expert CBSE teacher.

Generate a VERY DETAILED teaching script for ONE CLASS PERIOD.

Class: {grade}
Subject: {subject}
Chapter: {chapter}
Period Number: {period_no}
Pedagogy: {pedagogy}
Language of Instruction: {language}

Learning Outcomes:
{learning_outcomes}

Period Structure:
{PERIOD_STRUCTURE}

Integration Today:
{integration}

Rules:
- Exact teacher dialogue
- Questions to ask students
- Expected student responses
- Common misconceptions & corrections
- NO advice, ONLY classroom execution
- Plain text only
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {e}"

# -------------------------------------------------
# CHAPTER EXECUTION PLAN (PERIOD-BASED)
# -------------------------------------------------

def generate_chapter_execution_plan(
    grade,
    subject,
    chapter,
    required_periods,
    pedagogy,
    learning_outcomes,
    language
):
    """
    Creates a locked execution plan.
    Only ONE period unlocks at a time.
    """

    plan = {
        "grade": grade,
        "subject": subject,
        "chapter": chapter,
        "required_periods": required_periods,
        "periods": []
    }

    for i in range(required_periods):
        integration = None
        if i == 0:
            integration = "Language Integration"
        elif i == 1:
            integration = "Art / Subject Integration"
        elif i == required_periods - 1:
            integration = "Play-Based Activity"

        plan["periods"].append({
            "period_no": i + 1,
            "status": "unlocked" if i == 0 else "locked",
            "integration": integration,
            "learning_outcomes": learning_outcomes,
            "period_structure": PERIOD_STRUCTURE,
            "script": generate_teaching_script(
                grade,
                subject,
                chapter,
                i + 1,
                pedagogy,
                learning_outcomes,
                integration,
                language
            )
        })

    return plan
