def grade_band(grade):
    g = str(grade).upper().strip()
    if g in ["NURSERY", "LKG", "UKG", "KG", "PREP"]:
        return "FOUNDATIONAL"
    try:
        g = int(g)
        if g <= 3:
            return "PRIMARY"
        elif g <= 5:
            return "UPPER_PRIMARY"
        elif g <= 8:
            return "MIDDLE"
        else:
            return "SECONDARY"
    except:
        return "PRIMARY"


def generate_daily_plan(grade, subject, chapter, learning_outcomes, day, total_days):

    band = grade_band(grade)

    # ---------- SUBJECT PEDAGOGY ----------
    if subject.lower() in ["maths", "mathematics"]:
        focus = "concept understanding through examples and practice"
    elif subject.lower() in ["english", "hindi"]:
        focus = "language comprehension, vocabulary, and expression"
    elif subject.lower() in ["evs", "science"]:
        focus = "observation, explanation, and real-life connection"
    else:
        focus = "concept clarity and application"

    # ---------- LESSON FLOW ----------
    flow = []

    # ANCHOR
    flow.append({
        "phase": "ANCHOR (5 minutes)",
        "teacher_says": (
            f"Teacher introduces the chapter '{chapter}' by connecting it to students’ life. "
            f"Teacher asks questions related to students’ experiences relevant to this topic."
        ),
        "students_do": (
            "Students respond orally, share experiences, and listen to peers."
        ),
        "purpose": "Activate prior knowledge and curiosity."
    })

    # EXPLORE / EXPOSURE
    flow.append({
        "phase": "EXPOSURE (10 minutes)",
        "teacher_says": (
            f"Teacher explains the main idea of '{chapter}' using age-appropriate language. "
            f"The focus is on {focus}."
        ),
        "students_do": (
            "Students listen, observe examples, and note key points."
        ),
        "purpose": "Build initial understanding of the chapter."
    })

    # UNPACK LEARNING OUTCOMES
    for lo in learning_outcomes[:2]:
        flow.append({
            "phase": "UNPACK LEARNING (8 minutes)",
            "teacher_says": (
                f"Teacher explains the learning outcome: '{lo}'. "
                f"Teacher gives examples related to '{chapter}'."
            ),
            "students_do": (
                "Students answer guided questions and clarify doubts."
            ),
            "purpose": "Ensure learning outcomes are understood."
        })

    # PRACTICE
    flow.append({
        "phase": "GUIDED PRACTICE (7 minutes)",
        "teacher_says": (
            f"Teacher conducts a short activity or discussion based on '{chapter}'."
        ),
        "students_do": (
            "Students attempt tasks, discuss in pairs, or respond orally."
        ),
        "purpose": "Reinforce learning through practice."
    })

    # CLOSURE
    flow.append({
        "phase": "CLOSURE (5 minutes)",
        "teacher_says": (
            f"Teacher summarizes key ideas from '{chapter}' and previews the next lesson."
        ),
        "students_do": (
            "Students share one thing they learned today."
        ),
        "purpose": "Consolidate learning."
    })

    return {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "band": band
        },
        "flow": flow
    }
