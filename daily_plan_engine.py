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

    # ---------------- LANGUAGE & COGNITIVE TONE ----------------
    if band == "FOUNDATIONAL":
        tone = "simple, concrete, oral"
    elif band == "PRIMARY":
        tone = "guided, example-based"
    elif band == "UPPER_PRIMARY":
        tone = "structured explanation"
    elif band == "MIDDLE":
        tone = "analytical with reasoning"
    else:
        tone = "critical and exam-oriented"

    # ---------------- DEPTH FLOW ----------------
    flow = []

    # 1. ANCHOR
    flow.append({
        "phase": "ANCHOR – REAL LIFE CONNECTION",
        "minutes": 5,
        "teacher_script": (
            f"Teacher says: Today we begin '{chapter}'. "
            f"Before opening the book, think about a situation in real life related to this topic. "
            f"I will ask two students to share."
        ),
        "student_expected": (
            "Students respond orally using personal experiences. "
            "Some answers may be short or unrelated initially."
        ),
        "misconceptions": (
            "Students may think the topic is imaginary or unrelated to life."
        ),
        "teacher_correction": (
            "Teacher gently rephrases responses to show the real-life link."
        ),
        "board_work": "Topic title written clearly on board.",
        "skills": "Listening, Speaking",
        "purpose": "Emotional and contextual readiness"
    })

    # 2. EXPOSURE
    flow.append({
        "phase": "EXPOSURE – CONTENT IMMERSION",
        "minutes": 10,
        "teacher_script": (
            f"Teacher reads/explains the core content of '{chapter}' slowly. "
            f"Important sentences are paused and emphasized. "
            f"Teacher maintains eye contact and voice modulation."
        ),
        "student_expected": (
            "Students listen attentively, follow the text, and observe expressions."
        ),
        "misconceptions": (
            "Students may focus only on events, not ideas."
        ),
        "teacher_correction": (
            "Teacher asks: What does this tell us about people/situations?"
        ),
        "board_work": "Key sentence or idea underlined on board.",
        "skills": "Listening, Reading",
        "purpose": "Deep exposure to authentic content"
    })

    # 3. UNPACK LEARNING OUTCOMES
    for lo in learning_outcomes[:2]:
        flow.append({
            "phase": "UNPACK – LEARNING OUTCOME",
            "minutes": 8,
            "teacher_script": (
                f"Teacher explains the learning outcome: '{lo}'. "
                f"Examples are given from the chapter and daily life."
            ),
            "student_expected": (
                "Students answer guided questions and attempt to explain in their own words."
            ),
            "misconceptions": (
                "Students may repeat teacher words without understanding."
            ),
            "teacher_correction": (
                "Teacher asks follow-up WHY and HOW questions."
            ),
            "board_work": "Learning outcome written in simple words.",
            "skills": "Speaking, Understanding",
            "purpose": "Clarifying expected learning"
        })

    # 4. THINKING & REASONING
    flow.append({
        "phase": "THINK – REASON & JUDGE",
        "minutes": 8,
        "teacher_script": (
            "Teacher asks reasoning questions: Why did this happen? "
            "What could have been done differently?"
        ),
        "student_expected": (
            "Students justify answers; some may give emotional responses."
        ),
        "misconceptions": (
            "Students may answer without evidence."
        ),
        "teacher_correction": (
            "Teacher insists on answers supported by text or logic."
        ),
        "board_work": "Two reasoning questions written.",
        "skills": "Thinking, Speaking",
        "purpose": "Higher-order thinking"
    })

    # 5. PRACTICE / ENGAGEMENT
    flow.append({
        "phase": "ENGAGE – APPLY & EXPRESS",
        "minutes": 7,
        "teacher_script": (
            f"Teacher conducts an activity related to '{chapter}' "
            f"(short discussion / role-play / creative response)."
        ),
        "student_expected": (
            "Students participate actively and express understanding."
        ),
        "misconceptions": (
            "Students may focus on performance rather than concept."
        ),
        "teacher_correction": (
            "Teacher redirects focus back to learning idea."
        ),
        "board_work": "Activity instructions briefly noted.",
        "skills": "Speaking, Writing",
        "purpose": "Reinforcement through engagement"
    })

    # 6. CLOSURE
    flow.append({
        "phase": "CLOSE – CONSOLIDATE",
        "minutes": 5,
        "teacher_script": (
            "Teacher summarizes key learning in clear sentences "
            "and asks students to share one takeaway."
        ),
        "student_expected": (
            "Students respond with one-line summaries."
        ),
        "misconceptions": (
            "Students may recall facts but miss meaning."
        ),
        "teacher_correction": (
            "Teacher rephrases student answers for clarity."
        ),
        "board_work": "Summary point written.",
        "skills": "Listening, Speaking",
        "purpose": "Fix learning and retention"
    })

    return {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "band": band,
            "tone": tone
        },
        "flow": flow
    }
