# test/test_state_tracker.py

from detection.state_tracker import SessionState
import time

def test_log_and_finalize():
    session = SessionState("OP001", "MCH001")
    hazard = {
        "name": "engine_overheat",
        "description": "Engine too hot",
        "severity": "medium"
    }
    hazard_id = session.log_hazard(hazard)
    assert hazard_id is not None
    assert len(session.hazard_log) == 1

    session.log_response(hazard_id, "Cool Down", correct=True)
    session.log_response(hazard_id, "Ignore", correct=False)

    result = session.finalize()
    assert result["final_score"] == -1
    assert result["operator_id"] == "OP001"
