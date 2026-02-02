import streamlit as st
import pandas as pd
from openai import OpenAI

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Teach+ Pro", 
    page_icon="⏱️", 
    layout="wide"
)

st.title("⏱️ Teach+ Precision Planner")
st.markdown("### The Phase-Specific Micro-Planner")

# -----------------------------------------------------------------------------
# 2. LOAD DATABASE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Ensure this filename matches your uploaded file exactly
    file_path = "Teachshank_Master_Database_FINAL.tsv"
    try:
        df = pd.read_csv(file_path, sep='\t')
        return df
    except FileNotFoundError:
        st.error(f"⚠️ Critical Error: Could not find '{file_path}'. Please upload it to your GitHub repository.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# -----------------------------------------------------------------------------
# 3. SIDEBAR: PRECISION CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.header("🗓️ Scheduling Controls")

# A. Hierarchy Selection
grade_list = sorted(df['Grade'].astype(str).unique().tolist())
selected_grade = st.sidebar.selectbox("Select Grade", grade_list)

subject_list = sorted(df[df['Grade'].astype(str) == selected_grade]['Subject'].unique().tolist())
selected_subject = st.sidebar.selectbox("Select Subject", subject_list)

chapter_df = df[(df['Grade'].astype(str) == selected_grade) & (df['Subject'] == selected_subject)]
chapter_list = sorted(chapter_df['Chapter Name'].unique().tolist())
selected_chapter = st.sidebar.selectbox("Select Chapter", chapter_list)

# B. Smart Context
relevant_data = chapter_df[chapter_df['Chapter Name'] == selected_chapter]
learning_outcomes = relevant_data['Learning Outcomes'].dropna().tolist()

st.sidebar.markdown("---")

# C. Time & Sequence Controls
col1, col2 = st.sidebar.columns(2)
with col1:
    day_number = st.number_input("Academic Day", min_value=1, max_value=210, value=12)
with col2:
    duration = st.number_input("Duration (Mins)", min_value=30, max_value=60, value=40, step=5)

# D. Lesson Phase Selector (The Duplicate Killer)
# This lets the teacher specify if this is the Start, Middle, or End of the topic
lesson_phase = st.sidebar.radio(
    "Lesson Phase (prevents duplicate plans):",
    ["Part 1: Concept Launch (Intro)", 
     "Part 2: Deep Dive (Exploration)", 
     "Part 3: Application (Workbook/Practice)", 
     "Part 4: Assessment (Check for Understanding)"],
    index=0
)

# Display Learning Outcomes
with st.expander("🎯 Target Learning Outcomes for this Chapter", expanded=True):
    for lo in learning_outcomes:
        st.write(f"- {lo}")

# -----------------------------------------------------------------------------
# 4. THE PRECISION AI ENGINE
# -----------------------------------------------------------------------------
def generate_precision_plan(grade, subject, chapter, outcomes, day, duration, phase):
    
    # Calculate exact minute splits
    t_engage = int(duration * 0.15)  # 15%
    t_explore = int(duration * 0.30) # 30%
    t_explain = int(duration * 0.25) # 25%
    t_elaborate = int(duration * 0.20) # 20%
    t_evaluate = duration - (t_engage + t_explore + t_explain + t_elaborate) # Remainder

    prompt = f"""
    You are the 'Teach+' Precision Planner.
    
    CRITICAL INSTRUCTION:
    The user is asking for Day {day}. 
    This is **{phase}** of the chapter "{chapter}".
    **DO NOT** generate a generic introduction if the phase is "Deep Dive" or "Application".
    **DO NOT** repeat content from previous days. This specific lesson must fit the phase exactly.

    CONTEXT:
    - **Grade:** {grade}
    - **Subject:** {subject}
    - **Chapter:** {chapter}
    - **Outcomes:** {outcomes}
    - **Total Duration:** {duration} Minutes

    OUTPUT FORMAT (Markdown):

    ## 1. Lesson Metadata
    - **Micro-Topic:** (Specific sub-topic for Day {day})
    - **Cognitive Goal:** (What will they master by minute {duration}?)

    ## 2. The Timed 5E Script (Strict Timeline)

    ### ⏰ 00:00 - 00:{t_engage:02d} | I. ENGAGE (The Hook)
    - **Exact Script:** "Teacher says..."
    - **Physical Action:** (Prop/Movement)

    ### ⏰ 00:{t_engage:02d} - 00:{t_engage+t_explore:02d} | II. EXPLORE (The Activity)
    - **Activity Name:** ...
    - **Micro-Steps:**
      1. ...
      2. ...
    - **Teacher's Role:** (What to observe)

    ### ⏰ 00:{t_engage+t_explore:02d} - 00:{t_engage+t_explore+t_explain:02d} | III. EXPLAIN (The Concept)
    - **Board Work:** (What to draw/write)
    - **Scripted Explanation:** "Teacher explains..."
    - **Vocabulary Check:** ...

    ### ⏰ 00:{t_engage+t_explore+t_explain:02d} - 00:{t_engage+t_explore+t_explain+t_elaborate:02d} | IV. ELABORATE (Application)
    - **Differentiation:**
      - *Advanced:* ...
      - *Struggling:* ...

    ### ⏰ 00:{t_engage+t_explore+t_explain+t_elaborate:02d} - 00:{duration:02d} | V. EVALUATE (Exit Ticket)
    - **The Task:** ...
    - **Success Criteria:** ...

    Ensure the content is distinctly tailored to **{phase}**.
    """
    
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert curriculum designer. You hate generic lesson plans. You love precision."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6 # Lower temperature for more consistent, less random results
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------------------------------------------------------
# 5. GENERATE BUTTON
# -----------------------------------------------------------------------------
if st.button("🚀 Generate Timed Micro-Plan"):
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ OpenAI API Key is missing! Please add it to Streamlit Secrets.")
    else:
        with st.spinner(f"Designing Day {day_number} ({lesson_phase})..."):
            plan = generate_precision_plan(
                selected_grade, 
                selected_subject, 
                selected_chapter, 
                learning_outcomes, 
                day_number, 
                duration,
                lesson_phase
            )
            
            st.markdown("---")
            st.markdown(plan)
            
            st.download_button(
                label="📥 Download Timed Plan",
                data=plan,
                file_name=f"TeachPlus_G{selected_grade}_{selected_subject}_Day{day_number}.md",
                mime="text/markdown"
            )
