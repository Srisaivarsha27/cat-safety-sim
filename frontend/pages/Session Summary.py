import streamlit as st
from feedback.hf_feedback import generate_feedback

st.set_page_config(page_title="Session Summary", layout="wide")
st.title("📊 CAT Copilot - Session Summary")

# Load session summary from state
score = st.session_state.get("score", (0, 0, 0))
logs = st.session_state.get("logs", [])
task_name = st.session_state.get("task_name", "unknown")

st.subheader("✅ Final Score")
st.write(f"**Total Score:** `{score[0]} / {score[1]}` → **{score[2]}%**")

# Show action logs
st.subheader("📋 Action Log")
for entry in logs:
    st.markdown(f"""
    - **Hazard:** {entry['hazard']}
    - **Action Taken:** {entry['action']}
    - **Reward:** {entry['reward']} / {entry['max_score']}
    - **Result:** {entry['classification']}
    - **✅ Correct:** {"Yes" if entry['correct'] else "No"}
    ---
    """)

# Feedback summary
if st.button("📢 Generate AI Feedback Summary"):
    with st.spinner("Summarizing your performance..."):
        feedback = generate_feedback(task_name, logs, score)
        st.subheader("🤖 Feedback")
        st.success(feedback)
