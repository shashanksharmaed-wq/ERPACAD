# app.py
# ERPACAD – Academic Operating System
# Stable UI + DEPTH-CYCLE™ Lesson Viewer

import streamlit as st
from data_loader import load_data
from daily_plan_engine import generate_daily_plan

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="ERPACAD – Academic Engine",
    layout="wide"
)

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("DEPTH-CYCLE™ • CBSE-Aligned • Inspection-Ready")

# -------------------------------------------------
# LOAD DATA (SAFE)
# -------------------------------------------------
df = load_data()

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------
if "annual_plan" not in st.session_state:
    st.session_state.annual_plan = {}

if "completed_days" not in st.session_state:
    st.session_state.completed_days = {}

# -------------------------------------------------
# SELECTION PANEL
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox(
        "Class",
        sorted(df["grade"].unique())
    )

with col2:
    subject = st.selectbox(
        "Subject",
        sorted(df[df["grade"] == grade]["subject"].unique())
    )

with col3:
    academic_days = st.number_input(
        "Total Academic Working Days (School)",
        min_value=160,
        max_value=210,
        value=180
    )

st.divider()

# -------------------------------------------------
# CHAPTER SELECTION
# -------------------------------------------------
chapter_df = df[
    (df["grade"] == grade) &
    (df["subject"] == subject)
]

chapters = chapter_df["chapter"].unique().tolist()

if not chapters:
    st.warning("No chapters found for this class & subject.")
    st.stop()

chapter = st.selectbox("Select Chapter", chapters)

# -------------------------------------------------
# GENERATE ANNUAL PLAN (PER CHAPTER)
# -------------------------------------------------
if chapter not in st.session_state.annual_plan:
    # simple CBSE-safe heuristic
    lo_count = chapter_df[
        chapter_df["chapter"] == chapter
    ]["learning_outcome"].nunique()

    suggested_days = max(3, min(7, lo_count))

    st.session_state.annual_plan[chapter] = {
        "total_days": suggested_days
    }

total_days = st.session_state.annual_plan[chapter]["total_days"]

st.info(f"📅 **Suggested Duration:** {total_days} days")

# -------------------------------------------------
# DAY SELECTION (LOCKED FLOW)
# -------------------------------------------------
completed = st.session_state.completed_days.get(chapter, 0)

available_days = list(range(1, completed + 2))
available_days = [d for d in available_days if d <= total_days]

day = st.selectbox(
    "Select Day",
    available_days
)

# -------------------------------------------------
# GENERATE DAILY PLAN
# -------------------------------------------------
if st.button("🧠 Generate Daily Lesson Plan"):
    learning_outcomes = chapter_df[
        chapter_df["chapter"] == chapter
    ]["learning_outcome"].tolist()

    plan = generate_daily_plan(
        grade=grade,
        subject=subject,
        chapter=chapter,
        learning_outcomes=learning_outcomes,
        day=day,
        total_days=total_days
    )

    st.divider()
    st.header(
        f"📖 {chapter} — Day {day} of {total_days}"
    )

    # ---------------- META ----------------
    st.markdown("### 🔎 Lesson Metadata")
    st.write(plan["meta"])

    # ---------------- PHASES ----------------
    st.markdown("## 🧠 Detailed Teaching Script")

    for phase in plan["phases"]:
        with st.expander(
            f"{phase['code']} — {phase['name']} ({phase['minutes']} min)",
            expanded=True
        ):
            st.markdown("**Teacher Script**")
            for line in phase["teacher_script"]:
                st.write("•", line)

            st.markdown("**Expected Student Responses**")
            for resp in phase["expected_student_responses"]:
                st.write("•", resp)

            st.markdown("**Likely Misconceptions**")
            for m in phase["misconceptions"]:
                st.write("•", m)

            st.markdown("**Teacher Interventions**")
            for t in phase["teacher_interventions"]:
                st.write("•", t)

            st.markdown("**Assessment Evidence**")
            for a in phase["assessment_evidence"]:
                st.write("•", a)

    # ---------------- COMPLETE DAY ----------------
    if day == completed + 1:
        if st.button("✅ Mark Day Complete"):
            st.session_state.completed_days[chapter] = day
            st.success("Day marked complete. Next day unlocked.")
