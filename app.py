import streamlit as st
import pandas as pd
import os

from annual_plan_engine import generate_annual_plan
from daily_plan_engine import generate_daily_plan

st.set_page_config("ERPACAD", layout="wide")

DATA_PATH = "data/Teachshank_Master_Database_FINAL_v2.tsv"

# ---------------- AUTH ----------------
def authenticate(u, p):
    return u in st.secrets["users"] and st.secrets["users"][u] == p

def role_of(u):
    return st.secrets["roles"].get(u, "teacher")

# ---------------- DATA ----------------
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("❌ Data file missing")
        st.stop()
    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def detect(df, keys):
    for c in df.columns:
        for k in keys:
            if k in c:
                return c
    st.error(f"Missing column {keys}")
    st.stop()

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.progress = {}

# ---------------- LOGIN ----------------
if not st.session_state.login:
    st.title("🔐 ERPACAD Login")
    u = st.text_input("User ID")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(u, p):
            st.session_state.login = True
            st.session_state.user = u
            st.session_state.role = role_of(u)
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# ---------------- LOGOUT ----------------
with st.sidebar:
    st.write(f"👤 {st.session_state.user}")
    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.clear()
        st.rerun()

# ---------------- LOAD DATA ----------------
df = load_data()
CLASS = detect(df, ["class", "grade", "std"])
SUBJECT = detect(df, ["subject"])

# ---------------- TEACHER ----------------
if st.session_state.role == "teacher":

    st.title("📘 ERPACAD – Annual & Daily Planner")

    c1, c2, c3 = st.columns(3)
    with c1:
        grade = st.selectbox("Class", sorted(df[CLASS].unique()))
    with c2:
        subject = st.selectbox(
            "Subject",
            sorted(df[df[CLASS] == grade][SUBJECT].unique())
        )
    with c3:
        days = st.number_input("Academic Days", 160, 210, 180)

    if st.button("Generate Annual Plan"):
        plan = generate_annual_plan(df, grade, subject, days)

        if not plan["chapters"]:
            st.warning("No data found")
            st.stop()

        st.subheader("📅 Annual Plan")
        st.dataframe(pd.DataFrame(plan["chapters"]), use_container_width=True)

        st.divider()
        st.subheader("📘 Daily Lesson Plan")

        chapters = plan["chapters"]
        ch_name = st.selectbox("Chapter", [c["Chapter"] for c in chapters])

        ch_info = next(c for c in chapters if c["Chapter"] == ch_name)
        total = ch_info["Total Periods"]

        key = f"{grade}_{subject}_{ch_name}"
        day = st.session_state.progress.get(key, 1)

        if day > total:
            st.success("✅ Chapter Completed")
        else:
            daily = generate_daily_plan(ch_name, day, total, subject, grade)
            st.markdown(f"### 🗣️ {daily['title']}")

            for phase, time, t_script, s_act in daily["steps"]:
                with st.expander(f"{phase} ({time})"):
                    st.write("**Teacher:**", t_script)
                    st.write("**Students:**", s_act)

            if st.button("Mark Day Complete"):
                st.session_state.progress[key] = day + 1
                st.rerun()

# ---------------- PRINCIPAL ----------------
else:
    st.title("📊 Principal Dashboard")
    completed = len(st.session_state.progress)
    st.metric("Completed Lesson Days", completed)
    st.write("Syllabus completion tracking active.")
