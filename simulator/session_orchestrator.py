import time
import json
from simulator.telemetry_generator import generate_from_phase
from detection.hazard_rules import detect_hazards
from database.sqlite_logger import Logger
from simulator.task_scenarios import TASK_SCENARIOS

with open("config/hazard_config.json", "r") as f:
    HAZARD_CONFIG = json.load(f)

class SessionOrchestrator:
    def __init__(self, operator_id, task_name):
        self.operator_id = operator_id
        self.task_name = task_name
        self.session_id = f"{operator_id}_{int(time.time())}"
        self.logger = Logger()
        self.score = 0
        self.max_possible_score = 0
        self.hazard_count = 0
        self.action_log = []
        self.hazards_queue = []
        self.hazard_lookup = {}
        self.latest_telemetry = {}

        self.task = TASK_SCENARIOS[self.task_name]
        self.terrain = self.task["terrain"]
        self.machine_type = self.task["machine_type"]
        self.phases = iter(self.task["phases"])
        self.current_phase = next(self.phases, None)
        self.steps_remaining = self.current_phase["duration"] if self.current_phase else 0

        self.logger.start_session(self.session_id, self.operator_id, self.task_name)

    def next_step(self):
        if not self.current_phase:
            return None

        telemetry = generate_from_phase(
            self.current_phase["params"],
            {
                "terrain": self.terrain,
                "machine_type": self.machine_type,
                "task_name": self.task_name
            }
        )
        self.latest_telemetry = telemetry
        hazards = detect_hazards(telemetry)

        self.steps_remaining -= 1
        if self.steps_remaining <= 0:
            self.current_phase = next(self.phases, None)
            self.steps_remaining = self.current_phase["duration"] if self.current_phase else 0

        if hazards:
            hazard = hazards[0]
            self.hazard_count += 1
            hazard_id = self.logger.log_hazard(self.session_id, hazard["name"], hazard["description"])
            self.hazard_lookup[hazard_id] = hazard
            self.hazards_queue.append((hazard_id, hazard))
            return hazard_id, hazard

        return None

    def handle_action(self, hazard_id, action):
        hazard = self.hazard_lookup.get(hazard_id)
        config = HAZARD_CONFIG.get(hazard["name"], {})
        action_scores = config.get("actions", {})
        reward = action_scores.get(action, -2)
        max_score = max(action_scores.values(), default=0)

        classification = (
            "✅ Safe" if reward >= 2 else
            "⚠️ Mitigating" if reward > 0 else
            "❌ Unsafe"
        )

        self.score += reward
        self.max_possible_score += max_score

        self.logger.log_action(hazard_id, action, reward, classification)

        self.action_log.append({
            "hazard": hazard["name"],
            "action": action,
            "reward": reward,
            "max_score": max_score,
            "classification": classification,
            "correct": reward > 0
        })

        return {
            "reward": reward,
            "classification": classification
        }

    def end_session(self):
        self.logger.end_session(self.session_id, self.score, self.max_possible_score)
        percent = (self.score / self.max_possible_score * 100) if self.max_possible_score else 0
        return self.session_id, (self.score, self.max_possible_score, round(percent, 1)), self.action_log

