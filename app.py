import streamlit as st
from lesson_engine import load_data, get_classes, get_subjects, get_chapters

st.set_page_config(
    page_title="ERPACAD – Academic Planning Engine",
    layout="wide"
)

st.title("📘 ERPACAD – Academic Planning Engine")
st.caption("CBSE-aligned • Deep lesson planning • Teacher-ready")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- UI ----------------
col1, col2, col3 = st.columns(3)

with col1:
    grade = st.selectbox("Class", get_classes(df))

with col2:
    subject = st.selectbox("Subject", get_subjects(df, grade))

with col3:
    academic_days = st.number_input(
        "Academic Working Days (School-wide)",
        min_value=160,
        max_value=210,
        value=180
    )

st.divider()

st.subheader("📚 Chapters Covered")
chapters = get_chapters(df, grade, subject)

if chapters:
    for ch in chapters:
        st.markdown(f"- **{ch}**")
else:
    st.warning("No chapters found for this class & subject.")
