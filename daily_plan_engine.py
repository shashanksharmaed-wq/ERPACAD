def normalize_grade(grade):
    """Convert grade safely (handles NURSERY, KG, etc.)"""
    try:
        return int(grade)
    except:
        return grade


def generate_daily_plan(grade, subject, chapter, day, total_days):
    grade_norm = normalize_grade(grade)

    sections = [
        {
            "title": "Context & Connection",
            "minutes": 6,
            "teacher": (
                f"Teacher connects the theme of '{chapter}' to students’ real life. "
                "Asks reflective questions and builds curiosity."
            ),
            "students": (
                "Students share experiences, respond orally, and relate the theme "
                "to their surroundings."
            ),
            "purpose": "Activate prior knowledge and emotional engagement."
        },
        {
            "title": "Text Immersion",
            "minutes": 12,
            "teacher": (
                "Teacher reads the text aloud with expression. Important lines are "
                "paused and explained using examples and gestures."
            ),
            "students": (
                "Students listen carefully, follow the text, underline unfamiliar "
                "words, and note emotions."
            ),
            "purpose": "Build comprehension and listening skills."
        },
        {
            "title": "Concept & Vocabulary Deepening",
            "minutes": 10,
            "teacher": (
                "Teacher explains key words explicitly with meanings, sentence usage, "
                "and contextual relevance."
            ),
            "students": (
                "Students write meanings, frame sentences, and ask clarification questions."
            ),
            "purpose": "Develop language precision and clarity."
        },
        {
            "title": "Thinking & Reflection",
            "minutes": 8,
            "teacher": (
                "Teacher asks higher-order questions like WHY and WHAT IF to promote thinking."
            ),
            "students": (
                "Students discuss, justify opinions, and listen to peers."
            ),
            "purpose": "Build reasoning and moral understanding."
        },
        {
            "title": "Consolidation & Closure",
            "minutes": 4,
            "teacher": (
                "Teacher summarizes learning and previews next lesson."
            ),
            "students": (
                "Students recap learning in one sentence orally."
            ),
            "purpose": "Fix learning and ensure retention."
        }
    ]

    return {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days
        },
        "sections": sections
    }
