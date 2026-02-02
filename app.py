import streamlit as st
import pandas as pd
from openai import OpenAI
import math

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Teach+ Annual Planner", 
    page_icon="📅", 
    layout="wide"
)

st.title("📅 Teach+ Annual Curriculum Manager")
st.markdown("### Strategic Pacing & Micro-Planning")

# -----------------------------------------------------------------------------
# 2. LOAD DATABASE
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
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
# 3. SIDEBAR: HIGH-LEVEL SELECTION
# -----------------------------------------------------------------------------
st.sidebar.header("1️⃣ Select Class & Subject")

# A. Grade Selection
grade_list = sorted(df['Grade'].astype(str).unique().tolist())
selected_grade = st.sidebar.selectbox("Select Grade", grade_list)

# B. Subject Selection
subject_list = sorted(df[df['Grade'].astype(str) == selected_grade]['Subject'].unique().tolist())
selected_subject = st.sidebar.selectbox("Select Subject", subject_list)

# Filter Data for this selection
subject_data = df[
    (df['Grade'].astype(str) == selected_grade) & 
    (df['Subject'] == selected_subject)
]

# -----------------------------------------------------------------------------
# 4. INTELLIGENT CALENDAR GENERATOR
# -----------------------------------------------------------------------------
def generate_annual_calendar(data, total_days=180):
    """
    Allocates days to chapters based on the number of learning outcomes (Complexity Weighting).
    """
    # 1. Get Chapter List and Outcome Counts
    chapter_groups = data.groupby('Chapter Name')['Learning Outcomes'].count().reset_index()
    chapter_groups.columns = ['Chapter', 'Outcome_Count']
    
    # 2. Calculate Total Outcomes
    total_outcomes = chapter_groups['Outcome_Count'].sum()
    if total_outcomes == 0: return pd.DataFrame()

    # 3. Allocation Logic (Weighted Distribution)
    # Formula: (Chapter_Outcomes / Total_Outcomes) * 180 Days
    chapter_groups['Allocated_Days'] = (chapter_groups['Outcome_Count'] / total_outcomes) * total_days
    chapter_groups['Allocated_Days'] = chapter_groups['Allocated_Days'].apply(lambda x: math.ceil(x)) # Round up
    
    # 4. Create the Day-by-Day Schedule
    schedule = []
    current_day = 1
    
    # Organize chapters roughly by appearance (assuming DB order matters, if not we sort alphabetical)
    # Ideally, your DB would have a 'Sequence' column. For now, we take them as they appear.
    # We re-sort based on original dataframe index to preserve logical flow if it exists
    ordered_chapters = data['Chapter Name'].unique()
    
    for chap in ordered_chapters:
        row = chapter_groups[chapter_groups['Chapter'] == chap].iloc[0]
        days = int(row['Allocated_Days'])
        
        # Get Outcomes for this chapter
        outcomes = data[data['Chapter Name'] == chap]['Learning Outcomes'].tolist()
        
        for d in range(days):
            if current_day > total_days: break
            
            # Outcome Distribution: Rotate through outcomes for the days allocated
            daily_outcome = outcomes[d % len(outcomes)]
            
            # Determine Phase
            phase = "Concept Launch" if d == 0 else ("Assessment" if d == days-1 else "Deep Dive / Practice")
            
            schedule.append({
                "Day #": current_day,
                "Chapter": chap,
                "Focus Outcome": daily_outcome,
                "Lesson Phase": phase
            })
            current_day += 1
            
    return pd.DataFrame(schedule)

# Generate the Calendar
calendar_df = generate_annual_calendar(subject_data)

# -----------------------------------------------------------------------------
# 5. MAIN UI: ANNUAL CALENDAR DISPLAY
# -----------------------------------------------------------------------------
st.subheader(f"🗓️ Annual Pacing Guide: {selected_grade} - {selected_subject}")
st.info(f"Total Outcomes: {len(subject_data)} | Teaching Days: 180 | Logic: Weighted Allocation")

# Display the interactive dataframe
st.dataframe(
    calendar_df, 
    use_container_width=True, 
    height=400,
    column_config={
        "Day #": st.column_config.NumberColumn("Day", width="small"),
        "Chapter": st.column_config.TextColumn("Chapter Name", width="medium"),
        "Focus Outcome": st.column_config.TextColumn("Daily Learning Goal", width="large"),
        "Lesson Phase": st.column_config.TextColumn("Lesson Phase", width="small"),
    }
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. STEP 2: SELECT DAY TO PLAN
# -----------------------------------------------------------------------------
st.sidebar.header("2️⃣ Planner Controls")

# User selects a day number
selected_day_num = st.sidebar.number_input("Select Academic Day to Plan", min_value=1, max_value=180, value=1)

# Retrieve Context from the Generated Calendar
if not calendar_df.empty and selected_day_num <= len(calendar_df):
    day_row = calendar_df[calendar_df['Day #'] == selected_day_num].iloc[0]
    
    # Auto-fill context based on the calendar
    target_chapter = day_row['Chapter']
    target_outcome = day_row['Focus Outcome']
    target_phase = day_row['Lesson Phase']
    
    st.success(f"✅ **Planning Context for Day {selected_day_num}:**")
    col1, col2, col3 = st.columns(3)
    col1.metric("Chapter", target_chapter)
    col2.metric("Phase", target_phase)
    col3.metric("Topic", target_outcome[:50]+"...")
    
else:
    st.warning("Day out of range or no data.")
    st.stop()

duration = st.sidebar.slider("Duration (Mins)", 30, 60, 45)

# -----------------------------------------------------------------------------
# 7. AI GENERATION ENGINE
# -----------------------------------------------------------------------------
def generate_precision_plan(grade, subject, chapter, outcome, day, duration, phase):
    
    t_engage = int(duration * 0.15)
    t_explore = int(duration * 0.30)
    t_explain = int(duration * 0.25)
    t_elaborate = int(duration * 0.20)
    
    prompt = f"""
    You are the 'Teach+' Precision Planner.
    
    CRITICAL INSTRUCTION:
    The user is asking for **Day {day}** of the Annual Pacing Calendar.
    - **Chapter:** {chapter}
    - **Phase:** {phase} (Adjust tone accordingly: Intro vs. Practice vs. Test)
    - **Primary Outcome:** {outcome}

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
    - **Micro-Steps:** ...
    - **Teacher's Role:** (Observation Focus)

    ### ⏰ 00:{t_engage+t_explore:02d} - 00:{t_engage+t_explore+t_explain:02d} | III. EXPLAIN (The Concept)
    - **Board Work:** ...
    - **Scripted Explanation:** "Teacher explains..."

    ### ⏰ 00:{t_engage+t_explore+t_explain:02d} - 00:{t_engage+t_explore+t_explain+t_elaborate:02d} | IV. ELABORATE (Application)
    - **Task:** (Link to {outcome})

    ### ⏰ 00:{t_engage+t_explore+t_explain+t_elaborate:02d} - 00:{duration:02d} | V. EVALUATE (Exit Ticket)
    - **The Task:** ...
    """
    
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert curriculum designer. Precision is key."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------------------------------------------------------
# 8. GENERATE BUTTON
# -----------------------------------------------------------------------------
if st.button("🚀 Generate Plan for Day " + str(selected_day_num)):
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("⚠️ OpenAI API Key is missing!")
    else:
        with st.spinner(f"Designing Day {selected_day_num} ({target_chapter})..."):
            plan = generate_precision_plan(
                selected_grade, 
                selected_subject, 
                target_chapter, 
                target_outcome, 
                selected_day_num, 
                duration,
                target_phase
            )
            
            st.markdown("---")
            st.markdown(plan)
            
            st.download_button(
                label="📥 Download Plan",
                data=plan,
                file_name=f"TeachPlus_Day{selected_day_num}.md",
                mime="text/markdown"
            )
