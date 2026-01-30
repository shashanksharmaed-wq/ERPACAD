# engine.py
# Simple, stable lesson engine (no depth yet, no errors)

def generate_lesson(grade, subject, chapter, day):
    """
    Always returns the same safe structure.
    No conditionals. No parsing. No surprises.
    """

    lesson = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day
        },
        "blocks": [
            {
                "title": "Introduction",
                "teacher": (
                    f"Teacher introduces the chapter '{chapter}'. "
                    "Teacher explains what students will learn today."
                ),
                "students": (
                    "Students listen and respond to simple questions."
                ),
                "purpose": "Set context and focus attention."
            },
            {
                "title": "Main Teaching",
                "teacher": (
                    "Teacher explains the main idea using examples. "
                    "If a diagram is required, teacher draws it on the board."
                ),
                "students": (
                    "Students observe, ask doubts, and copy key points."
                ),
                "purpose": "Build basic understanding."
            },
            {
                "title": "Closure",
                "teacher": (
                    "Teacher summarizes the lesson and checks understanding."
                ),
                "students": (
                    "Students answer orally."
                ),
                "purpose": "Confirm learning."
            }
        ]
    }

    return lesson
