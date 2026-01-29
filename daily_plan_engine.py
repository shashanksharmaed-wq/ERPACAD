# daily_plan_engine.py
# ERPACAD – Deep Daily Lesson Plan Engine
# Safe for Nursery–Class 12

# -------------------------------------------------
# GRADE NORMALIZATION
# -------------------------------------------------

GRADE_MAP = {
    "NURSERY": 0,
    "LKG": 1,
    "UKG": 2,
    "1": 3,
    "2": 4,
    "3": 5,
    "4": 6,
    "5": 7,
    "6": 8,
    "7": 9,
    "8": 10,
    "9": 11,
    "10": 12,
    "11": 13,
    "12": 14
}

# -------------------------------------------------
# DEPTH PROFILE (AGE-AWARE)
# -------------------------------------------------

def get_depth_profile(grade: str):
    grade_key = str(grade).strip().upper()
    level = GRADE_MAP.get(grade_key, 5)  # default middle level

    if level <= 2:  # Nursery / LKG / UKG
        return "FOUNDATIONAL"
    elif level <= 5:  # Class 1–3
        return "CONCRETE"
    elif level <= 8:  # Class 4–6
        return "STRUCTURED"
    elif level <= 11:  # Class 7–9
        return "ANALYTICAL"
    else:  # Class 10–12
        return "CRITICAL"

# -------------------------------------------------
# MAIN DAILY PLAN GENERATOR
# -------------------------------------------------

def generate_daily_plan(
    grade,
    subject,
    chapter,
    learning_outcomes,
    day,
    total_days
):
    depth = get_depth_profile(grade)

    plan = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "depth_level": depth
        },
        "sections": []
    }

    # ---------------- FOUNDATIONAL ----------------
    if depth == "FOUNDATIONAL":
        plan["sections"] = [
            {
                "title": "Experience & Talk",
                "minutes": 10,
                "teacher": "Teacher introduces the topic using objects, pictures, gestures, and voice modulation.",
                "students": "Children observe, name objects, repeat words, and respond orally.",
                "purpose": "Language exposure and sensory engagement."
            },
            {
                "title": "Story / Rhyme Time",
                "minutes": 10,
                "teacher": "Teacher narrates the full story/rhyme clearly with actions and pauses.",
                "students": "Children listen, repeat key lines, enact with gestures.",
                "purpose": "Listening comprehension and memory building."
            },
            {
                "title": "Play-Based Activity",
                "minutes": 10,
                "teacher": "Teacher conducts a guided game linked to the concept.",
                "students": "Children participate joyfully following rules.",
                "purpose": "Learning through play."
            }
        ]

    # ---------------- CONCRETE ----------------
    elif depth == "CONCRETE":
        plan["sections"] = [
            {
                "title": "Context Connection",
                "minutes": 8,
                "teacher": "Teacher connects the lesson to students’ real-life experiences.",
                "students": "Students share examples from home or surroundings.",
                "purpose": "Activate prior knowledge."
            },
            {
                "title": "Concept Clarification",
                "minutes": 15,
                "teacher": "Teacher explains ideas with examples, visuals, and questioning.",
                "students": "Students listen, respond, and note keywords.",
                "purpose": "Concept understanding."
            },
            {
                "title": "Guided Practice",
                "minutes": 10,
                "teacher": "Teacher facilitates structured activity or worksheet discussion.",
                "students": "Students apply learning individually or in pairs.",
                "purpose": "Skill reinforcement."
            }
        ]

    # ---------------- STRUCTURED ----------------
    elif depth == "STRUCTURED":
        plan["sections"] = [
            {
                "title": "Concept Building",
                "minutes": 12,
                "teacher": "Teacher explains key ideas step-by-step using board and visuals.",
                "students": "Students ask questions and take notes.",
                "purpose": "Structured understanding."
            },
            {
                "title": "Application Task",
                "minutes": 15,
                "teacher": "Teacher assigns activity applying the concept.",
                "students": "Students solve, discuss, and justify answers.",
                "purpose": "Concept application."
            }
        ]

    # ---------------- ANALYTICAL ----------------
    elif depth == "ANALYTICAL":
        plan["sections"] = [
            {
                "title": "Critical Reading / Observation",
                "minutes": 12,
                "teacher": "Teacher guides students through text/data analysis.",
                "students": "Students infer meanings and identify patterns.",
                "purpose": "Analytical thinking."
            },
            {
                "title": "Discussion & Reasoning",
                "minutes": 15,
                "teacher": "Teacher conducts guided discussion using why/how questions.",
                "students": "Students defend viewpoints with evidence.",
                "purpose": "Reasoning and communication."
            }
        ]

    # ---------------- CRITICAL ----------------
    else:
        plan["sections"] = [
            {
                "title": "Inquiry & Debate",
                "minutes": 20,
                "teacher": "Teacher presents problem or inquiry question.",
                "students": "Students analyze, debate, and justify positions.",
                "purpose": "Higher-order thinking."
            },
            {
                "title": "Reflection & Synthesis",
                "minutes": 15,
                "teacher": "Teacher facilitates synthesis of ideas.",
                "students": "Students summarize learning and reflect.",
                "purpose": "Concept consolidation."
            }
        ]

    return plan
