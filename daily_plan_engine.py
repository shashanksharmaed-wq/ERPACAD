# daily_plan_engine.py
# ERPACAD – DEPTH-CYCLE™ Lesson Generator
# FINAL, STABLE VERSION

from typing import Dict, List

# -------------------------------------------------
# DEPTH PROFILE
# -------------------------------------------------

def get_depth_profile(grade: int) -> str:
    if grade <= 3:
        return "PRIMARY"
    elif grade <= 5:
        return "UPPER_PRIMARY"
    elif grade <= 8:
        return "MIDDLE"
    else:
        return "SECONDARY"


# -------------------------------------------------
# PUBLIC API (DO NOT RENAME)
# -------------------------------------------------

def generate_daily_plan(
    grade: int,
    subject: str,
    chapter: str,
    learning_outcomes: List[str],
    day: int,
    total_days: int,
    period_minutes: int = 40
) -> Dict:
    """
    Generates ONE DAY lesson plan using ERPACAD DEPTH-CYCLE™
    This is the ONLY function app.py should import.
    """

    depth = get_depth_profile(grade)
    exam_mode = grade >= 9

    plan = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "period_minutes": period_minutes,
            "depth_profile": depth,
            "exam_relevance": exam_mode
        },
        "phases": []
    }

    # -------------------------------
    # D — DISCOVER CONTEXT
    # -------------------------------
    plan["phases"].append({
        "code": "D",
        "name": "Discover Context",
        "minutes": 6,
        "teacher_script": [
            f"Think about a real-life situation connected to '{chapter}'.",
            "How do people usually react in such situations?"
        ],
        "expected_student_responses": [
            "Students share observations from daily life."
        ],
        "misconceptions": [
            "Students may think this is only a story, not real-life related."
        ],
        "teacher_interventions": [
            "Guide students to see the connection between life and learning."
        ],
        "assessment_evidence": [
            "Students verbally connect topic to lived experience."
        ]
    })

    # -------------------------------
    # E — EXPOSE CORE CONTENT
    # -------------------------------
    plan["phases"].append({
        "code": "E",
        "name": "Expose Core Content",
        "minutes": 10,
        "teacher_script": [
            f"I will now read and explain an important part of '{chapter}'.",
            "Listen carefully to the language and ideas."
        ],
        "expected_student_responses": [
            "Students listen and identify key ideas."
        ],
        "misconceptions": [
            "Students may focus only on events, not meaning."
        ],
        "teacher_interventions": [
            "Pause to explain difficult words and ideas."
        ],
        "assessment_evidence": [
            "Students can explain the idea in their own words."
        ]
    })

    # -------------------------------
    # P — PROBE THINKING
    # -------------------------------
    probe_questions = [
        f"Why do you think the characters behave the way they do in '{chapter}'?",
        "What choice would you make in the same situation?"
    ]

    if depth in ["MIDDLE", "SECONDARY"]:
        probe_questions.append(
            "What does this situation reveal about human behaviour or society?"
        )

    plan["phases"].append({
        "code": "P",
        "name": "Probe Thinking",
        "minutes": 8,
        "teacher_script": probe_questions,
        "expected_student_responses": [
            "Students justify answers using reasons."
        ],
        "misconceptions": [
            "Students may answer emotionally without evidence."
        ],
        "teacher_interventions": [
            "Ask follow-up questions to push deeper reasoning."
        ],
        "assessment_evidence": [
            "Students support answers with examples or context."
        ]
    })

    # -------------------------------
    # T — TRANSFORM UNDERSTANDING
    # -------------------------------
    transform_tasks = [
        "Students write one sentence connecting the lesson to their own life.",
        "Students discuss how the idea applies beyond the classroom."
    ]

    if exam_mode:
        transform_tasks.append(
            "Students link the theme to possible exam-style questions."
        )

    plan["phases"].append({
        "code": "T",
        "name": "Transform Understanding",
        "minutes": 10,
        "teacher_script": [
            "Let us now apply what we have understood."
        ],
        "expected_student_responses": transform_tasks,
        "misconceptions": [
            "Students may repeat textbook language without understanding."
        ],
        "teacher_interventions": [
            "Model one clear, original example."
        ],
        "assessment_evidence": [
            "Original student responses showing application."
        ]
    })

    # -------------------------------
    # H — HARVEST EVIDENCE
    # -------------------------------
    harvest_notes = [
        "Students summarise the lesson in one sentence."
    ]

    if exam_mode:
        harvest_notes.append(
            "Teacher highlights how this learning can be assessed in exams."
        )

    plan["phases"].append({
        "code": "H",
        "name": "Harvest Evidence",
        "minutes": 6,
        "teacher_script": [
            "Let us reflect on what we learned today."
        ],
        "expected_student_responses": [
            "Students share key takeaways."
        ],
        "misconceptions": [
            "Students may recall facts but miss deeper meaning."
        ],
        "teacher_interventions": [
            "Rephrase responses to reinforce clarity."
        ],
        "assessment_evidence": harvest_notes
    })

    return plan
