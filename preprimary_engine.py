# preprimary_engine.py
# ERPACAD – Pre-Primary Readiness Engine
# One continuous teaching script, no steps, no loops, no fragile structure

def generate_preprimary_lesson(class_name, subject):
    title = f"{class_name} {subject} – Readiness Experience"
    duration = "Flexible (teacher observes readiness, not the clock)"

    if class_name == "LKG" and subject == "Literacy":
        script = """
The teacher waits quietly until all children are seated and calm.
She does not rush silence and does not clap or call out.

She stands where every child can clearly see her face and mouth.
She smiles and speaks softly:

"Children… today we are going to listen very carefully."

She pauses and touches her ear to model listening.
She waits until children mirror her calm.

She produces the sound /b/ slowly, exaggerating lip movement.
She does not say the letter name.
She repeats the sound once more after a pause.

Some children may say “B”.
She gently says, “Only sound. Not name.”

She asks quietly, “Where have you heard this sound?”
She listens to all responses without correcting harshly.

She then draws a simple ball on the board.
She points and says slowly, “Ball… /b/.”

She places two pictures: ball and apple.
She stays silent for a few seconds.
She produces the sound /b/ once and waits.

Children begin to point.
She observes without speaking.

She calls one child at a time, places three pictures,
produces one sound, and waits.

She does not help immediately.
She allows thinking time.

The lesson ends calmly.
She says, “Your ears worked very hard today.”

By the end, the child can independently hear a beginning sound
and identify a matching object without prompting.
"""

    elif class_name == "LKG" and subject == "Numeracy":
        script = """
The teacher places a few counters on the table.
She does not speak immediately.

She places one counter and says softly, “One.”
She pauses.
She places another and says, “One… two.”

She gives three counters to a child and watches silently.
She does not correct verbally.
She models again if needed.

She later asks individual children to give “two” or “three”.
She waits patiently for independent response.

The lesson ends when children show one-to-one correspondence
without copying others.
"""

    elif class_name == "NURSERY" and subject == "Literacy":
        script = """
The teacher sits at the children’s eye level.
She uses facial expressions and gestures more than words.

She produces familiar sounds rhythmically.
She uses objects to anchor meaning.

Children respond through pointing, sound attempts, or smiles.

The lesson ends when children show recognition and engagement,
not verbal accuracy.
"""

    elif class_name == "UKG" and subject == "Literacy":
        script = """
The teacher reads a short sentence with expression.
She asks what sound children heard first.

She introduces the letter symbol gently.
She draws it and traces while speaking the sound.

Children attempt independently on slate or in the air.

The lesson ends when children connect sound to symbol
without teacher cues.
"""

    else:
        script = """
This readiness experience focuses on calm engagement,
observation, and independent child response.
"""

    return {
        "title": title,
        "duration": duration,
        "script": script.strip()
    }
