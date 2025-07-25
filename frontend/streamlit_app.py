import streamlit as st
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulator.session_orchestrator import SessionOrchestrator

# Optional: if gemini_feedback will be filled in later
try:
    from feedback.hf_feedback import generate_feedback
except ImportError:
    def generate_feedback(*args, **kwargs):
        return "Feedback module not implemented."

with open("config/hazard_config.json", "r") as f:
    HAZARD_CONFIG = json.load(f)

st.set_page_config(page_title="Cat Copilot Simulator", layout="wide")
st.title("🚜 CAT Copilot Safety Simulator")

# Init session state
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
    st.session_state.current_hazard = None
    st.session_state.logs = []
    st.session_state.score = (0, 0, 0)

# Sidebar for session start
st.sidebar.header("🧑‍💼 Operator Info")
operator_id = st.sidebar.text_input("Operator ID", value="demo")

task_map = {
    "Trenching": "dig_trench_rocky",
    "Truck Loading": "load_truck_flat",
    "Slope Navigation": "navigate_slope_incline"
}
task_choice = st.sidebar.selectbox("Select Task", list(task_map.keys()))
task_name = task_map[task_choice]

if st.sidebar.button("Start New Session"):
    st.session_state.orchestrator = SessionOrchestrator(operator_id, task_name)
    st.session_state.current_hazard = None
    st.session_state.logs = []
    st.session_state.score = (0, 0, 0)
    st.success(f"New session started for '{task_name}'.")

# Main simulation area
orch = st.session_state.orchestrator
if orch:
    st.subheader("🧭 Current Task State")
    st.markdown(f"""
    - **Task Name:** `{orch.task_name}`
    - **Terrain:** `{orch.terrain}`
    - **Machine:** `{orch.machine_type}`
    - **Current Phase:** `{orch.current_phase['name'] if orch.current_phase else 'None'}`
    - **Steps Remaining:** `{orch.steps_remaining}`
    """)

    with st.expander("📡 Telemetry Data"):
        st.json(orch.latest_telemetry)

    if st.session_state.current_hazard is None:
        if st.button("▶️ Next Step"):
            result = orch.next_step()
            if result:
                st.session_state.current_hazard = result
                hazard_id, hazard = result
                st.warning(f"⚠️ Hazard Detected: `{hazard['name']}`\n\n> {hazard['description']}")
            else:
                st.info("No hazard detected.")
    else:
        hazard_id, hazard = st.session_state.current_hazard
        st.warning(f"⚠️ Hazard Detected: `{hazard['name']}`\n\n> {hazard['description']}")
        config = HAZARD_CONFIG.get(hazard["name"], {})
        action_scores = config.get("actions", {})

        st.write("### 🧠 Choose Your Action:")
        for action in action_scores:
            if st.button(f"🛠 {action}"):
                result = orch.handle_action(hazard_id, action)
                if result["reward"] > 0:
                    st.success(f"{result['classification']} ✅ (Reward: {result['reward']})")
                else:
                    st.error(f"{result['classification']} ❌ (Penalty: {result['reward']})")
                st.session_state.logs.append(orch.action_log[-1])
                st.session_state.current_hazard = None
                st.rerun()

    progress = orch.score / orch.max_possible_score if orch.max_possible_score else 0
    progress = max(0.0, min(progress, 1.0))  # Clamp between 0.0 and 1.0
    st.progress(progress)

    if st.button("📦 End Session"):
        sess_id, score, logs = orch.end_session()
        st.session_state.score = score
        st.session_state.logs = logs
        st.session_state.task_name = orch.task_name
        st.session_state.orchestrator = None
        st.success("Session complete! Redirecting to summary...")
        st.info("👉 Use the sidebar to navigate to **'summary_page'**.")



# Final Summary
if st.session_state.logs:
    st.subheader("📋 Action Log")
    for entry in st.session_state.logs:
        st.markdown(f"""
        - **Hazard:** `{entry['hazard']}`
        - **Action Taken:** `{entry['action']}`
        - **Reward:** `{entry['reward']} / {entry['max_score']}`
        - **Result:** `{entry['classification']}`
        - ✅ **Correct:** {"Yes" if entry['correct'] else "No"}
        ---""")

    st.subheader("📊 Final Score")
    score = st.session_state.score
    st.metric("Final Score", f"{score[0]} / {score[1]}", f"{score[2]}%")
