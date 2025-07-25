# detection/state_tracker.py

import time
from typing import Dict, List

class SessionState:
    def __init__(self, operator_id: str, machine_id: str):
        self.operator_id = operator_id
        self.machine_id = machine_id
        self.start_time = time.time()
        self.hazard_log: List[Dict] = []
        self.action_log: List[Dict] = []
        self.score = 0
        self.active_hazards = set()

    def log_hazard(self, hazard: Dict):
        hazard_id = f"{hazard['name']}_{int(time.time())}"
        if hazard["name"] not in self.active_hazards:
            self.hazard_log.append({
                "id": hazard_id,
                "name": hazard["name"],
                "description": hazard["description"],
                "severity": hazard["severity"],
                "timestamp": time.time()
            })
            self.active_hazards.add(hazard["name"])
            return hazard_id
        return None

    def log_response(self, hazard_id: str, action: str, correct: bool):
        self.action_log.append({
            "hazard_id": hazard_id,
            "action": action,
            "timestamp": time.time(),
            "correct": correct
        })
        if correct:
            self.score += 2
        else:
            self.score -= 3

    def finalize(self) -> Dict:
        return {
            "operator_id": self.operator_id,
            "machine_id": self.machine_id,
            "duration": round(time.time() - self.start_time, 2),
            "hazards": self.hazard_log,
            "actions": self.action_log,
            "final_score": self.score
        }
