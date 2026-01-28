import streamlit as st
import pandas as pd
import os

from annual_plan_engine import generate_annual_plan
from daily_plan_engine import generate_daily_plan

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

DATA_PATH = "data/Teachshank_Master_Database_FINAL_v2.tsv"

# =====================================================
# AUTH
# =====================================================
def authenticate(user, pwd):
    return user in st.secrets["users"] and st.secrets["users"][user] == pwd

def get_role(user):
    return st.secrets["roles"].get(user, "teacher")

# =====================================================
# DATA HELPERS
# =====================================================
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("❌ Data file not found")
        st.stop()
    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def detect_column(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k in col:
                return col
    st.error(f"❌ Missing column: {keywords}")
    st.stop()

# =====================================================
# SESSION INIT
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.progress = {}

# =====================================================
# LOGIN
# =====================================================
if not st.session_state.logged_in:
    st.title("🔐 ERPACAD Login")

    with st.form("login"):
        u = st.text_input("User ID")
        p = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if authenticate(u, p):
            st.session_state.logged_in = True
            st.session_state.user = u
            st.session_state.role = get_role(u)
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# =====================================================
# LOGOUT
# =====================================================
with st.sidebar:
    st.write(f"👤 Logged in as **{st.session_state.user}**")
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()

# =====================================================
# LOAD DATA
# =====================================================
df = load_data()
CLASS_COL = detect_column(df, ["class", "grade", "std"])
SUBJECT_COL = detect_column(df, ["subject"])

# =====================================================
# TEACHER VIEW
# =====================================================
if st.session_state.role == "teacher":

    st.title("📘 ERPACAD – Annual & Daily Lesson Planner")

    c1, c2, c3 = st.columns(3)

    with c1:
        grade = st.selectbox("Class", sorted(df[CLASS_COL].unique()))

    with c2:
        subject = st.selectbox(
            "Subject",
            sorted(df[df[CLASS_COL] == grade][SUBJECT_COL].unique())
        )

    with c3:
        academic_days = st.number_input(
            "Academic Working Days",
            min_value=160,
            max_value=210,
            value=180
        )

    if st.button("📅 Generate Annual Plan"):
        plan = generate_annual_plan(df, grade, subject, academic_days)

        if not plan["chapters"]:
            st.warning("No syllabus data found")
            st.stop()

        st.subheader("📅 Annual Academic Plan")
        st.dataframe(pd.DataFrame(plan["chapters"]), use_container_width=True)

        st.divider()
        st.subheader("📖 Daily Lesson Plan (Auto-sequenced)")

        chapters = plan["chapters"]
        chapter_name = st.selectbox(
            "Select Chapter",
            [c["Chapter"] for c in chapters]
        )

        chapter_info = next(c for c in chapters if c["Chapter"] == chapter_name)
        total_days = chapter_info["Total Periods"]

        progress_key = f"{grade}_{subject}_{chapter_name}"
        current_day = st.session_state.progress.get(progress_key, 1)

        if current_day > total_days:
            st.success("✅ Chapter Completed")
        else:
            daily = generate_daily_plan(
                chapter_name,
                current_day,
                total_days,
                subject,
                grade
            )

            st.markdown(f"## 🗣️ {daily['title']}")
            st.caption(f"⏱ {daily['period_duration']} | {daily['pedagogy']}")

            for block in daily["lesson_flow"]:
                with st.expander(f"{block['phase']} ({block['time']})"):
                    st.markdown("**Teacher says:**")
                    st.write(block["teacher_script"])

                    st.markdown("**Students respond:**")
                    st.write(block["student_response"])

                    st.markdown("**Learning Intent:**")
                    st.write(block["learning_intent"])

            st.info(daily["teacher_guidance"])

            if st.button("✅ Mark Day Complete"):
                st.session_state.progress[progress_key] = current_day + 1
                st.rerun()

# =====================================================
# PRINCIPAL VIEW
# =====================================================
else:
    st.title("📊 Principal Dashboard")

    completed = len(st.session_state.progress)
    st.metric("Completed Lesson Days", completed)

    st.write("Syllabus progression is being tracked class-wise and chapter-wise.")
