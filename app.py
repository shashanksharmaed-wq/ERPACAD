import streamlit as st
import pandas as pd

from lesson_engine import load_data, generate_chapter_plan
from annual_plan_engine import generate_annual_plan

st.set_page_config(page_title="ERPACAD", layout="wide")

df = load_data()

# ---------------- SESSION ----------------
for k in ["annual_plan", "annual_locked", "chapter_plans"]:
    if k not in st.session_state:
        st.session_state[k] = {} if k == "chapter_plans" else None

# ---------------- SIDEBAR ----------------
role = st.sidebar.selectbox("Login as", ["Principal", "Teacher"])
grade = st.sidebar.selectbox("Class", sorted(df["grade"].unique()))
subject = st.sidebar.selectbox(
    "Subject", sorted(df[df["grade"] == grade]["subject"].unique())
)
language = st.sidebar.selectbox("Language", ["English", "Hindi"])
pedagogy = st.sidebar.selectbox("Pedagogy", ["LEARN360", "BLOOMS", "5E"])

# ================= PRINCIPAL =================
if role == "Principal":
    st.header("📅 Annual Academic Plan")

    total_days = st.number_input(
        "Total Working Days", min_value=160, max_value=210, value=180
    )

    if st.button("Generate Annual Plan"):
        st.session_state.annual_plan = generate_annual_plan(
            df, grade, subject, total_days
        )
        st.session_state.annual_locked = False

    if st.session_state.annual_plan:
        st.dataframe(pd.DataFrame(st.session_state.annual_plan))
        if st.button("🔒 Lock Annual Plan"):
            st.session_state.annual_locked = True
            st.success("Annual plan locked.")

# ================= TEACHER =================
if role == "Teacher":
    if not st.session_state.annual_locked:
        st.warning("Annual plan not locked by Principal.")
        st.stop()

    chapters = [c["chapter"] for c in st.session_state.annual_plan]
    chapter = st.selectbox("Chapter", chapters)

    days_allowed = next(
        c["suggested_days"] for c in st.session_state.annual_plan
        if c["chapter"] == chapter
    )

    if chapter not in st.session_state.chapter_plans:
        st.session_state.chapter_plans[chapter] = generate_chapter_plan(
            df, grade, subject, chapter,
            days_allowed, pedagogy, language
        )

    plan = st.session_state.chapter_plans[chapter]

    current_day = next((d for d in plan["days"] if d["status"] == "unlocked"), None)

    if not current_day:
        st.success("🎉 Chapter completed.")
        st.stop()

    st.subheader(f"{chapter} – Day {current_day['day_no']} of {plan['total_days']}")

    st.table(pd.DataFrame(
        current_day["period_structure"],
        columns=["Phase", "Minutes"]
    ))

    st.markdown("### Learning Outcomes")
    for lo in current_day["learning_outcomes"]:
        st.write(f"- {lo}")

    st.markdown("### Lesson Flow")
    table = []
    for p, m in current_day["period_structure"]:
        table.append({
            "Phase": p,
            "Time": f"{m} min",
            "Teacher Action": "As per script",
            "Questions": "Embedded",
            "Assessment": "Formative"
        })
    st.dataframe(pd.DataFrame(table), use_container_width=True)

    st.markdown("### Teaching Script")
    st.text_area("Script", current_day["script"], height=350)

    if st.button("Mark Day Completed"):
        idx = current_day["day_no"] - 1
        plan["days"][idx]["status"] = "completed"
        if idx + 1 < len(plan["days"]):
            plan["days"][idx + 1]["status"] = "unlocked"
        st.success("Day completed.")
        st.rerun()
