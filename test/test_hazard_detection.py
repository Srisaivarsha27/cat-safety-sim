# test/test_hazard_detection.py

from detection.hazard_rules import (
    detect_seatbelt_violation,
    detect_overheating,
    detect_hazards
)

def test_seatbelt_violation():
    t = {"speed": 5.0, "seatbelt": "unfastened"}
    hazard = detect_seatbelt_violation(t)
    assert hazard and hazard["name"] == "seatbelt_violation"

def test_engine_overheat():
    t = {"engine_temp": 90}
    hazard = detect_overheating(t)
    assert hazard and hazard["name"] == "engine_overheat"

def test_no_hazard_when_values_safe():
    t = {
        "speed": 1.0,
        "seatbelt": "fastened",
        "engine_temp": 70,
        "fuel_level": 50,
        "pressure": 850,
        "proximity": 5.0,
        "brake_status": True,
        "terrain": "flat"
    }
    hazards = detect_hazards(t)
    assert len(hazards) == 0
