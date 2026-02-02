import streamlit as st
import pandas as pd
from openai import OpenAI

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Teach+", 
    page_icon="🎓", 
    layout="wide"
)

# App Title & Branding
st.title("🎓 Teach+ Lesson Architect")
st.markdown("### The AI Academic Director")

# -----------------------------------------------------------------------------
# 2. LOAD DATABASE FROM GITHUB
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # NOTE: Keep this filename matching exactly what you uploaded to GitHub
    file_path = "Teachshank_Master_Database_FINAL.tsv"
    try:
        # Load TSV (Tab Separated Values)
        df = pd.read_csv(file_path, sep='\t')
        return df
    except FileNotFoundError:
        st.error(f"⚠️ Critical Error: Could not find '{file_path}'. Please upload it to your GitHub repository.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()  # Stop app if data isn't loaded

# -----------------------------------------------------------------------------
# 3. SIDEBAR: CURRICULUM CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.header("🗓️ Teach+ Curriculum Controls")

# A. Grade Selection
grade_list = sorted(df['Grade'].astype(str).unique().tolist())
selected_grade = st.sidebar.selectbox("Select Grade", grade_list)

# B. Subject Selection (Filtered by Grade)
subject_list = sorted(df[df['Grade'].astype(str) == selected_grade]['Subject'].unique().tolist())
selected_subject = st.sidebar.selectbox("Select Subject", subject_list)

# C. Chapter Selection (Filtered by Subject)
chapter_df = df[
    (df['Grade'].astype(str) == selected_grade) & 
    (df['Subject'] == selected_subject)
]
chapter_list = sorted(chapter_df['Chapter Name'].unique().tolist())
selected_chapter = st.sidebar.selectbox("Select Chapter", chapter_list)

# D. Learning Outcomes Preview
relevant_data = chapter_df[chapter_df['Chapter Name'] == selected_chapter]
learning_outcomes = relevant_data['Learning Outcomes'].dropna().tolist()

st.sidebar.markdown("---")
day_number = st.sidebar.number_input("Academic Day (e.g., Day 12 of 180)", min_value=1, max_value=210, value=12)
duration = st.sidebar.slider("Class Duration (Minutes)", 30, 90, 45)

# Display context in main area
with st.expander("📚 View Selected Learning Outcomes", expanded=True):
    if learning_outcomes:
        for lo in learning_outcomes:
            st.write(f"- {lo}")
    else:
        st.write("No specific outcomes listed for this selection.")

# -----------------------------------------------------------------------------
# 4. THE TEACH+ AI ENGINE
# -----------------------------------------------------------------------------
def generate_micro_plan(grade, subject, chapter, outcomes, day, duration):
    # This prompt is engineered for "Micro-Scripting" depth
    prompt = f"""
    You are the 'Teach+' AI Academic Director.
    Your task is to generate a 'Micro-Lesson Script' that beats the quality of premium frameworks like Chrysalis/EDAC.
    
    TEACHING CONTEXT:
    - **Grade:** {grade}
    - **Subject:** {subject}
    - **Chapter:** {chapter}
    - **Day:** {day} of 180 (Term 1)
    - **Duration:** {duration} Minutes
    - **Target Learning Outcomes:** {outcomes}
    
    STRICT OUTPUT FORMAT (Use Markdown):
    
    ## 1. Metadata
    - **The Why:** (Why are we teaching this? Link to real life)
    - **The What:** (Specific Concept)
    - **The Who:** (Cognitive readiness of this age group)

    ## 2. The 5E Micro-Script (Must be dialogue-heavy)
    
    ### I. ENGAGE (First 15%)
    - **The Hook Action:** (Specific physical prop or movement)
    - **Teacher Script:** "Write exactly what the teacher says here..."
    
    ### II. EXPLORE (Next 25%)
    - **The Activity:** (Hands-on, sensory, or inquiry-based)
    - **Micro-Instruction:** "Step-by-step instructions for the students..."
    
    ### III. EXPLAIN (Next 20%)
    - **Concept & Vocabulary:** (Define specific terms)
    - **Misconception Alert:** (What will students likely get wrong?)
    
    ### IV. ELABORATE (Next 20%)
    - **Application:** (Cross-curricular link or real-world problem)
    - **Differentiation:** - *Advanced:* (Challenge task)
        - *Struggling:* (Support strategy)
        
    ### V. EVALUATE (Final 20%)
    - **Exit Ticket:** (A quick check for understanding)
    - **Success Criteria:** (How do we know they learned it?)

    Do not summarize. Script the lesson dialogue for the teacher.
    """
    
    try:
        # Use Streamlit Secrets for the API Key
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",  # Recommended for maximum depth
            messages=[
                {"role": "system", "content": "You are a master pedagogue specializing in 5E lesson planning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------------------------------------------------------
# 5. GENERATE BUTTON
# -----------------------------------------------------------------------------
if st.button("✨ Generate Teach+ Micro-Plan"):
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ OpenAI API Key is missing! Please add it to Streamlit Secrets.")
    else:
        with st.spinner("Teach+ is designing your micro-lesson..."):
            plan = generate_micro_plan(
                selected_grade, 
                selected_subject, 
                selected_chapter, 
                learning_outcomes, 
                day_number, 
                duration
            )
            
            st.markdown("---")
            st.markdown(plan)
            
            # Download capability
            st.download_button(
                label="📥 Download Teach+ Plan",
                data=plan,
                file_name=f"TeachPlus_Plan_{selected_grade}_{selected_subject}_Day{day_number}.md",
                mime="text/markdown"
            )
