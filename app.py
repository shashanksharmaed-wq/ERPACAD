import streamlit as st
import pandas as pd
import os

from annual_plan_engine import generate_annual_plan

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

DATA_PATH = "data/Teachshank_Master_Database_FINAL_v2.tsv"

# ---------------- SAFE LOAD ----------------
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


df = load_data()

CLASS_COL = detect_column(df, ["class", "grade", "std"])
SUBJECT_COL = detect_column(df, ["subject"])

# ---------------- UI ----------------
st.title("📘 ERPACAD – Academic Planning Engine")

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

# ---------------- ACTION ----------------
if st.button("📅 Generate Annual Plan"):
    plan = generate_annual_plan(
        df,
        selected_class,
        selected_subject,
        academic_days
    )

    if not plan["chapters"]:
        st.warning(plan.get("message", "No plan generated"))
    else:
        st.success("✅ Annual Plan Generated (CBSE-aligned, period-based)")

        st.markdown(f"""
        **Weekly Periods:** {plan['weekly_periods']}  
        **Total Periods (Year):** {plan['total_periods']}
        """)

        plan_df = pd.DataFrame(plan["chapters"])
        st.dataframe(plan_df, use_container_width=True)
