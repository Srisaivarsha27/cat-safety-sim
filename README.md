# 🏗️ CAT Safety Simulator

A construction operator training and safety evaluation simulator built for realistic hazard detection, action logging, and reinforcement-style learning evaluation.

## 🚀 Overview

**CAT Safety Simulator** replicates real-world machine operation scenarios to train and evaluate construction equipment operators. It helps assess decision-making under safety-critical conditions using hazard detection, feedback generation, and scoring mechanisms based on operator responses.

This project provides:

* A dynamic simulation environment with configurable phases and terrain
* Real-time hazard detection based on telemetry
* Reward-based scoring for reinforcement learning style assessment
* Auto-generated feedback reports using a lightweight local language model

---

## 📦 Features

✅ Hazard detection from synthetic telemetry
✅ Operator action handling and reward computation
✅ Real-time scoring and risk classification
✅ GPT-based feedback generation (offline using `gpt2` or similar open-source model)
✅ Streamlit dashboard for simulation control and session summaries
✅ SQLite-based logging and history tracking
✅ Easily extensible for new tasks, terrains, and hazards

---

## 🧠 Architecture

```
Simulator ───▶ Telemetry Generator ───▶ Hazard Detection ───▶ Scoring + Feedback
   ▲                                                        ▼
User Actions ◀───────────────────────────────────────────────┘
```

### Key Modules:

* `simulator/`: Defines task phases and generates telemetry per phase
* `detection/`: Applies rule-based hazard detection
* `database/`: Logs sessions, hazards, and actions to SQLite
* `feedback/`: Generates natural language feedback from performance
* `frontend/`: Streamlit UI for running and reviewing simulations
* `config/`: Configurable hazard-action-reward maps

---

## 🧪 Example Tasks

* **Ladder Setup**
* **Trench Digging**
* **Rocky Terrain Handling**
* **Fall Protection**

Hazards include: `proximity_alert`, `hydraulic_pressure_surge`, `unsecured_ladder`, etc.

Each hazard is mapped to possible actions and scored using a reward system like:

```json
"proximity_alert": {
  "actions": {
    "Ignore": -2,
    "Reverse": 2,
    "Alert Supervisor": 1
  }
}
```

---

## 💡 How It Works

1. **Telemetry Simulation**: Each task has defined phases with parameters. Telemetry is synthetically generated.
2. **Hazard Detection**: Rules are applied to detect unsafe conditions.
3. **User Action Logging**: User responds with an action when a hazard is detected.
4. **Reward Assignment**: Actions are scored based on risk mitigation.
5. **Session Logging**: All actions and hazards are logged.
6. **Feedback Generation**: A GPT model produces a natural-language safety report.

---

## ✍️ Feedback Example

> **Summary**: The operator showed partial compliance with safety norms.
> **Strengths**: Timely reaction to proximity alerts.
> **Mistakes**: Continued operation during hydraulic pressure surge.
> **Recommendations**: Always pause and alert the supervisor in high-risk conditions.
> **Risk Awareness Score**: 6/10

---

## 📷 UI Preview

<img width="1888" height="830" alt="image" src="https://github.com/user-attachments/assets/776ae0ef-c73b-4683-aa0e-d8105ac6b809" />

<img width="1074" height="740" alt="image" src="https://github.com/user-attachments/assets/490ae728-69f1-46cf-846b-6ad62ae63a64" />

---

## 🛠️ Setup

```bash
git clone https://github.com/yourname/cat-safety-sim.git
cd cat-safety-sim
python -m venv .venv
.venv\Scripts\activate    # On Windows
pip install -r requirements.txt
```

Optionally add your Hugging Face token to `.env`:

```
HF_TOKEN=your_token_here
```

---

## ▶️ Running the Simulator

```bash
streamlit run frontend/streamlit_app.py
```

You can view the web UI at [http://localhost:8501](http://localhost:8501)

---

## 🔍 Project Structure

```
cat-safety-sim/
├── config/                 # Hazard and machine configuration
├── database/               # SQLite logger
├── detection/              # Rule-based hazard detection
├── feedback/               # Feedback generation module
├── frontend/               # Streamlit frontend
├── simulator/              # Task simulation engine
├── test/                   # Unit tests
├── requirements.txt
├── README.md
```

---

## 🧠 Future Enhancements

* RL agent training via gym-style interface
* Video telemetry with real-world data
* Integration with vLLM/TGI for fast inference
* Multi-agent or multiplayer mode

---

## 👩‍💻 Authors

* [Your Name](https://github.com/yourusername)
* [Collaborator Name](https://github.com/theirusername)

---
