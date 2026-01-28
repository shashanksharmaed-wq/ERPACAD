import streamlit as st
import pandas as pd
import os

from annual_plan_engine import generate_annual_plan

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

DATA_PATH = "data/Teachshank_Master_Database_FINAL_v2.tsv"

# =====================================================
# AUTH HELPERS
# =====================================================
def authenticate(username, password):
    users = st.secrets["users"]
    if username in users and users[username] == password:
        return True
    return False


def get_role(username):
    return st.secrets["roles"].get(username, "teacher")


# =====================================================
# DATA HELPERS
# =====================================================
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ Data file missing at: {DATA_PATH}")
        st.stop()

    df = pd.read_csv(DATA_PATH, sep="\t")
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def detect_column(df, keywords):
    for col in df.columns:
        for k in keywords:
            if k in col:
                return col
    st.error(f"❌ Required column missing: {keywords}")
    st.stop()


# =====================================================
# SESSION INIT
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# =====================================================
# LOGIN SCREEN
# =====================================================
if not st.session_state.logged_in:
    st.title("🔐 ERPACAD Login")

    with st.form("login_form"):
        username = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = get_role(username)
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid ID or Password")

    st.stop()

# =====================================================
# LOGOUT BUTTON
# =====================================================
with st.sidebar:
    st.write(f"👤 Logged in as **{st.session_state.user}**")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
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

    st.title("📘 ERPACAD – Annual Academic Plan")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_class = st.selectbox(
            "Class",
            sorted(df[CLASS_COL].unique())
        )

    with col2:
        selected_subject = st.selectbox(
            "Subject",
            sorted(
                df[df[CLASS_COL] == selected_class][SUBJECT_COL].unique()
            )
        )

    with col3:
        academic_days = st.number_input(
            "Academic Working Days (School-wide)",
            min_value=160,
            max_value=210,
            value=180
        )

    if st.button("📅 Generate Annual Plan"):
        plan = generate_annual_plan(
            df,
            selected_class,
            selected_subject,
            academic_days
        )

        if not plan["chapters"]:
            st.warning("No syllabus data found")
        else:
            st.success("Annual Plan Generated (CBSE-aligned)")

            st.markdown(f"""
            **Weekly Periods:** {plan['weekly_periods']}  
            **Total Periods (Year):** {plan['total_periods']}
            """)

            st.dataframe(
                pd.DataFrame(plan["chapters"]),
                use_container_width=True
            )

            st.info(
                "ℹ️ Daily lesson plans will strictly follow this annual pacing."
            )

# =====================================================
# PRINCIPAL VIEW
# =====================================================
elif st.session_state.role == "principal":

    st.title("📊 Principal Dashboard")

    st.info(
        "This dashboard will show syllabus completion status.\n\n"
        "Daily lesson completion will be added next."
    )

    st.metric("Total Classes", df[CLASS_COL].nunique())
    st.metric("Total Subjects", df[SUBJECT_COL].nunique())

    st.write("📘 Annual planning data is active and CBSE-aligned.")

