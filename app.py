import streamlit as st
import pandas as pd
from daily_plan_engine import generate_daily_plan

st.set_page_config(page_title="ERPACAD", layout="wide")

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("CBSE-aligned • Deep lesson planning • Teacher-ready")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/master.tsv", sep="\t")
    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

# ---------- SELECTORS ----------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox("Class", sorted(df["Grade"].unique(), key=str))

with col2:
    subject = st.selectbox(
        "Subject",
        sorted(df[df["Grade"] == grade]["Subject"].unique())
    )

with col3:
    total_days = st.number_input(
        "Total Days for Chapter",
        min_value=1,
        max_value=20,
        value=7
    )

chapter = st.selectbox(
    "Chapter",
    df[(df["Grade"] == grade) & (df["Subject"] == subject)]["Chapter Name"].unique()
)

day = st.selectbox(
    "Select Day",
    list(range(1, total_days + 1))
)

st.divider()

# ---------- GENERATE DAILY PLAN ----------
plan = generate_daily_plan(
    grade=grade,
    subject=subject,
    chapter=chapter,
    day=day,
    total_days=total_days
)

st.header(f"🧠 {chapter} – Day {day} of {total_days}")

for section in plan["sections"]:
    with st.expander(f"{section['title']} ({section['minutes']} min)"):
        st.markdown(f"**Teacher does:** {section['teacher']}")
        st.markdown(f"**Students do:** {section['students']}")
        st.markdown(f"**Purpose:** {section['purpose']}")

st.success("✅ Lesson plan generated successfully")
