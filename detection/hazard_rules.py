# detection/hazard_rules.py

from typing import List, Dict

def detect_seatbelt_violation(t: Dict) -> Dict | None:
    if t.get("speed", 0) > 1.0 and t.get("seatbelt") != "fastened":
        return {
            "name": "seatbelt_violation",
            "severity": "high",
            "description": "Seatbelt not fastened while vehicle is moving."
        }

def detect_overheating(t: Dict) -> Dict | None:
    if t.get("engine_temp", 0) > 85:
        return {
            "name": "engine_overheat",
            "severity": "medium",
            "description": f"Engine temperature exceeded safe limit ({t['engine_temp']}°C)."
        }

def detect_low_fuel(t: Dict) -> Dict | None:
    if t.get("fuel_level", 100) < 15:
        return {
            "name": "low_fuel",
            "severity": "medium",
            "description": f"Fuel level low: {t['fuel_level']}%."
        }

def detect_proximity_alert(t: Dict) -> Dict | None:
    if t.get("proximity", 100) < 2.0:
        return {
            "name": "proximity_alert",
            "severity": "critical",
            "description": f"Obstacle/person too close: {t['proximity']}m."
        }

def detect_outside_geofence(t: Dict) -> Dict | None:
    if t.get("geofence_zone") == "outside":
        return {
            "name": "geofence_violation",
            "severity": "medium",
            "description": "Machine outside assigned geofence zone."
        }

def detect_brake_on_slope(t: Dict) -> Dict | None:
    if t.get("terrain") == "inclined" and not t.get("brake_status", True):
        return {
            "name": "brake_not_applied_on_slope",
            "severity": "high",
            "description": "Brakes not engaged while on slope."
        }

def detect_pressure_surge(t: Dict) -> Dict | None:
    if t.get("pressure", 0) > 900:
        return {
            "name": "hydraulic_pressure_surge",
            "severity": "medium",
            "description": f"Hydraulic pressure too high: {t['pressure']} kPa."
        }

def detect_idle_timeout(t: Dict) -> Dict | None:
    if t.get("idle_time", 0) > 60:
        return {
            "name": "idle_timeout",
            "severity": "low",
            "description": f"Machine idling too long: {t['idle_time']} seconds."
        }

def detect_vibration_spike(t: Dict) -> Dict | None:
    if t.get("vibration_level", 0) > 2.2:
        return {
            "name": "vibration_spike",
            "severity": "medium",
            "description": f"Machine vibration too high: {t['vibration_level']}."
        }

# Add more rules here...

# Main engine
HAZARD_RULES = [
    detect_seatbelt_violation,
    detect_overheating,
    detect_low_fuel,
    detect_proximity_alert,
    detect_outside_geofence,
    detect_brake_on_slope,
    detect_pressure_surge,
    detect_idle_timeout,
    detect_vibration_spike
]

def detect_hazards(telemetry: Dict) -> List[Dict]:
    return [hazard for rule in HAZARD_RULES if (hazard := rule(telemetry))]
