import streamlit as st
import os, json
from lesson_engine import (
    load_data,
    calculate_annual_plan,
    generate_daywise_plan,
    enrich_lesson_content
)
from approvals import submit_for_approval, approve_lesson, is_locked

st.set_page_config(page_title="ERPACAD", layout="wide")
st.title("ERPACAD – Advanced Academic Engine")

df = load_data()
APPROVAL_DIR = "approvals"

role = st.sidebar.selectbox("Login as", ["Teacher", "Principal"])

# ================= TEACHER =================
if role == "Teacher":
    st.subheader("👩‍🏫 Teacher Panel")

    grade = st.selectbox("Class", sorted(df["grade"].unique()))
    subject = st.selectbox("Subject", sorted(df[df["grade"] == grade]["subject"].unique()))
    annual_plan = calculate_annual_plan(df, grade, subject)

    chapter = st.selectbox("Chapter", list(annual_plan.keys()))
    pedagogy = st.selectbox(
        "Pedagogy Framework",
        ["LEARN360", "BLOOMS", "5E"]
    )

    meta = {
        "grade": grade,
        "subject": subject,
        "chapter": chapter,
        "pedagogy": pedagogy
    }

    if is_locked(meta):
        st.error("🔒 Lesson plan is approved and locked.")
        st.stop()

    days = st.number_input("Number of Days", min_value=1, value=annual_plan[chapter])
    period_minutes = st.selectbox("Period Duration", [30, 35, 40, 45])
    use_ai = st.checkbox("Generate detailed teaching script (AI)")

    if st.button("Generate Lesson Plan"):
        plans = generate_daywise_plan(
            df, grade, subject, chapter, days, period_minutes, pedagogy
        )

        if use_ai:
            plans = [
                enrich_lesson_content(p, grade, subject, chapter)
                for p in plans
            ]

        st.session_state["plans"] = plans
        st.session_state["meta"] = meta

    if "plans" in st.session_state:
        for p in st.session_state["plans"]:
            st.markdown(f"## {p['day']} ({p['pedagogy']})")

            for phase, text in p["lesson_flow"].items():
                st.markdown(f"### {phase}")
                st.write(text)

            st.markdown("### Learning Outcomes")
            st.write(p["learning_outcomes"])

            st.markdown("### Assessment")
            st.write(p["assessment"])

            st.markdown("### SEL Focus")
            st.write(p["sel"])

            if use_ai:
                st.markdown("### Detailed Teaching Script")
                st.write(p["ai_detail"])

        if st.button("📤 Submit to Principal"):
            submit_for_approval(st.session_state["meta"], st.session_state["plans"])
            st.success("Submitted for approval")

# ================= PRINCIPAL =================
if role == "Principal":
    st.subheader("🧑‍💼 Principal Dashboard")

    records = []
    if os.path.exists(APPROVAL_DIR):
        for f in os.listdir(APPROVAL_DIR):
            if f.endswith(".json"):
                with open(f"{APPROVAL_DIR}/{f}", "r") as file:
                    records.append(json.load(file))

    pending = [r for r in records if r["status"] == "PENDING"]

    for r in pending:
        with st.expander(
            f"{r['meta']['grade']} | {r['meta']['subject']} | "
            f"{r['meta']['chapter']} ({r['meta']['pedagogy']})"
        ):
            remark = st.text_area("Principal Remark", key=r["id"])
            if st.button("Approve & Lock", key=f"a_{r['id']}"):
                approve_lesson(r["id"], remark)
                st.rerun()
