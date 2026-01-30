# engine.py
# Single-Act Lesson Engine (Stable, Expandable, Error-proof)

def generate_lesson(grade, subject, chapter, day):
    """
    Generates ONE continuous teaching act.
    No steps, no blocks, no loops.
    """

    teacher_flow = (
        f"Teacher begins the lesson by clearly announcing the chapter '{chapter}'. "
        "Teacher first creates attention by asking students to sit quietly and focus. "
        "Teacher then connects the topic to a familiar real-life situation using simple language. "
        "After this, the teacher explains the core idea slowly, using examples students already know. "
        "If the concept requires a visual explanation, the teacher draws a simple diagram on the board "
        "and explains each part while drawing. "
        "Teacher pauses at natural points to ask short questions like 'Why do you think this happens?' "
        "or 'What did you notice here?'. "
        "If students give incorrect answers, the teacher does not say 'wrong' but rephrases the idea "
        "and gives another example to guide understanding. "
        "Towards the end, the teacher summarizes the key learning in clear sentences and tells students "
        "what they should remember from today’s lesson."
    )

    student_flow = (
        "Students listen carefully, observe the board work, and respond orally to teacher questions. "
        "Students attempt answers even if unsure and adjust their understanding based on teacher guidance. "
        "Students recall examples and relate them to their own experiences."
    )

    outcome_check = (
        "By the end of the lesson, students should be able to explain the main idea of the chapter "
        "in their own words and answer at least one reasoning-based question correctly."
    )

    tlm_note = (
        "If required, teacher uses blackboard/whiteboard for drawing simple diagrams. "
        "No printed or digital material is mandatory."
    )

    return {
        "meta": {
            "grade": grade,
            "subject": subject,
            "chapter": chapter,
            "day": day
        },
        "teacher_flow": teacher_flow,
        "student_flow": student_flow,
        "tlm": tlm_note,
        "outcome_check": outcome_check
    }
