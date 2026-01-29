# daily_plan_engine.py

def get_depth_profile(grade):
    grade = str(grade).upper()

    if grade in ["NURSERY", "LKG", "UKG"]:
        return "FOUNDATIONAL"
    elif grade in ["1", "2", "3"]:
        return "PRIMARY"
    elif grade in ["4", "5"]:
        return "UPPER_PRIMARY"
    elif grade in ["6", "7", "8"]:
        return "MIDDLE"
    else:
        return "SECONDARY"


def generate_daily_plan(
    grade,
    subject,
    chapter,
    day,
    total_days,
    learning_outcomes=None
):
    depth = get_depth_profile(grade)

    plan = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "depth_profile": depth
        },
        "sections": []
    }

    # ---------- FOUNDATIONAL ----------
    if depth == "FOUNDATIONAL":
        plan["sections"] = [
            {
                "title": "Experience & Play",
                "teacher": (
                    f"Teacher sets up a play-based situation related to '{chapter}'. "
                    "Uses real objects, gestures, facial expressions, and voice modulation."
                ),
                "students": (
                    "Children explore freely, respond verbally or through actions."
                ),
                "purpose": "Build comfort and intuitive understanding"
            },
            {
                "title": "Language Exposure",
                "teacher": (
                    "Teacher narrates the story/rhyme fully, slowly, with pauses. "
                    "Key words are repeated clearly."
                ),
                "students": (
                    "Children listen, repeat key words, mimic actions."
                ),
                "purpose": "Oral language development"
            }
        ]

    # ---------- PRIMARY ----------
    elif depth == "PRIMARY":
        plan["sections"] = [
            {
                "title": "Context Building",
                "teacher": (
                    f"Teacher narrates the full story of '{chapter}' with expression. "
                    "Stops at key moments to ask prediction questions."
                ),
                "students": (
                    "Students listen, predict outcomes, connect with prior experiences."
                ),
                "purpose": "Comprehension & engagement"
            },
            {
                "title": "Concept Clarification",
                "teacher": (
                    "Teacher explains important words, situations, and ideas "
                    "using examples from the story."
                ),
                "students": (
                    "Students explain meanings in their own words."
                ),
                "purpose": "Vocabulary & concept clarity"
            }
        ]

    # ---------- MIDDLE & SECONDARY ----------
    else:
        plan["sections"] = [
            {
                "title": "Deep Reading",
                "teacher": (
                    f"Teacher reads and explains '{chapter}' line by line, "
                    "highlighting ideas, tone, and author intent."
                ),
                "students": (
                    "Students annotate, ask questions, infer meanings."
                ),
                "purpose": "Critical reading"
            },
            {
                "title": "Concept Analysis",
                "teacher": (
                    "Teacher facilitates discussion on themes, causes, effects, "
                    "and real-world relevance."
                ),
                "students": (
                    "Students justify answers with text evidence."
                ),
                "purpose": "Analytical thinking"
            }
        ]

    return plan
