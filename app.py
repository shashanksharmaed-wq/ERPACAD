import streamlit as st
import pandas as pd
import json
from auth import login, logout
from lesson_engine import generate_deep_daily_plan
from annual_plan_engine import generate_annual_plan

DATA_PATH = "data/master.tsv"
PROGRESS_FILE = "progress.json"

st.set_page_config(page_title="ERPACAD", layout="wide")

# ---------- LOGIN ----------
if not login():
    st.stop()

st.sidebar.write(f"👤 Logged in as {st.session_state.user}")
if st.sidebar.button("Logout"):
    logout()

# ---------- LOAD DATA ----------
df = pd.read_csv(DATA_PATH, sep="\t")
df.columns = [c.strip().lower() for c in df.columns]

# ---------- SELECT ----------
grade = st.selectbox("Class", sorted(df["class"].unique()))
subject = st.selectbox(
    "Subject",
    sorted(df[df["class"] == grade]["subject"].unique())
)

academic_days = st.number_input(
    "Academic Working Days (School-wide)",
    min_value=160,
    max_value=210,
    value=180
)

# ---------- ANNUAL PLAN ----------
if st.button("Generate Annual Plan"):
    annual_plan = generate_annual_plan(df, grade, subject, academic_days)
    st.session_state.annual_plan = annual_plan
    st.session_state.current_day = 1

# ---------- DAILY VIEW ----------
if "annual_plan" in st.session_state:
    plan = st.session_state.annual_plan
    chapter = plan[0]["chapter"]
    total_days = plan[0]["days"]
    los = plan[0]["los"]

    day = st.session_state.get("current_day", 1)

    lesson = generate_deep_daily_plan(chapter, day, total_days, los)

    st.header(lesson["title"])

    for phase, content in lesson.items():
        if phase == "title":
            continue
        with st.expander(f"{phase} ({content['time']})", expanded=True):
            st.markdown("**Teacher says:**")
            for t in content["teacher_says"]:
                st.write("- ", t)

            st.markdown("**Students do:**")
            for s in content["students_do"]:
                st.write("- ", s)

            if content["board_work"]:
                st.markdown("**Board work:**")
                for b in content["board_work"]:
                    st.write("- ", b)

            if content["questions"]:
                st.markdown("**Questions:**")
                for q in content["questions"]:
                    st.write("- ", q)

    if st.button("Mark Day Complete"):
        st.session_state.current_day += 1
        st.rerun()
