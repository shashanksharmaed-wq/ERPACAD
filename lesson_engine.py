def generate_deep_daily_plan(
    grade: int,
    subject: str,
    chapter: str,
    learning_outcomes: list,
    day: int,
    total_days: int
):
    """
    Generates a deeply scripted, minute-wise daily lesson plan.
    """

    # ---------------- TIME BUDGET ----------------
    PERIOD_MINUTES = 40

    # ---------------- CORE CONTENT ----------------
    story_block = (
        "Lencho was a poor farmer who lived in a small house on the crest "
        "of a low hill. From his fields, he could see the river and the ripe "
        "cornfields dotted with the flowers that always promised a good harvest..."
    )

    key_words = [
        "faith",
        "hailstorm",
        "harvest",
        "postmaster",
        "charity"
    ]

    misconceptions = [
        "Faith means expecting miracles without effort",
        "Charity is only about money",
        "God directly sends letters or money"
    ]

    # ---------------- LESSON STRUCTURE ----------------
    lesson = {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day,
            "total_days": total_days,
            "period_duration": PERIOD_MINUTES
        },

        "learning_outcomes_focused": learning_outcomes,

        "lesson_flow": [
            {
                "phase": "Contextual Hook",
                "minutes": 5,
                "teacher_says": (
                    "Today I want to ask you a question. "
                    "Have you ever believed very strongly in something, "
                    "even when others doubted you?"
                ),
                "students_do": (
                    "Students raise hands and share short personal experiences."
                ),
                "purpose": "Emotionally connect students to the theme of faith."
            },

            {
                "phase": "Activate Prior Knowledge",
                "minutes": 5,
                "teacher_says": (
                    "We have read stories where characters face problems. "
                    "What usually helps them — luck, people, or belief?"
                ),
                "students_do": (
                    "Students discuss answers orally. Teacher writes keywords on board."
                ),
                "purpose": "Bridge prior stories with current chapter."
            },

            {
                "phase": "Reveal Content",
                "minutes": 10,
                "teacher_says": (
                    "Listen carefully as I read the story aloud.\n\n"
                    f"{story_block}"
                ),
                "students_do": (
                    "Students listen attentively. Some follow along in the textbook."
                ),
                "purpose": "Expose students to authentic literary text."
            },

            {
                "phase": "Engage Deeply",
                "minutes": 7,
                "teacher_says": (
                    "Why do you think Lencho wrote a letter to God instead of asking people?"
                ),
                "students_do": (
                    "Students respond. Teacher probes answers using why/how questions."
                ),
                "purpose": "Encourage inference and character analysis."
            },

            {
                "phase": "Facilitate Practice",
                "minutes": 5,
                "teacher_says": (
                    "Let us look at these important words from the story:\n"
                    + ", ".join(key_words)
                ),
                "students_do": (
                    "Students write meanings in their own words and use them in sentences."
                ),
                "purpose": "Build vocabulary and language skills."
            },

            {
                "phase": "Use in Life",
                "minutes": 4,
                "teacher_says": (
                    "Think of a situation where belief helped someone act courageously."
                ),
                "students_do": (
                    "Students share examples from real life or imagination."
                ),
                "purpose": "Transfer learning beyond the classroom."
            },

            {
                "phase": "Learning Check & Closure",
                "minutes": 4,
                "teacher_says": (
                    "Today we learned that faith can give strength, "
                    "but people also help one another."
                ),
                "students_do": (
                    "Students summarize the lesson in one sentence orally."
                ),
                "purpose": "Consolidate understanding."
            }
        ],

        "anticipated_misconceptions": misconceptions,

        "teacher_notes": (
            "Encourage respectful discussion. Avoid religious preaching. "
            "Focus on values and human support systems."
        )
    }

    return lesson
