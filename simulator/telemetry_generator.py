import json, random, time
from datetime import datetime
from pathlib import Path
from simulator.task_scenarios import TASK_SCENARIOS

TELEMETRY_FILE = Path("simulator") / "telemetry.json"
DEFAULT_INTERVAL = 1.5  # seconds between telemetry ticks

MACHINE_ID = "EXC001"
OPERATOR_ID = "OP1001"

# Persistent session states
SESSION_STATE = {
    "seatbelt": "fastened",
    "geofence_zone": "inside",
    "brake_status": True,
    "engine_hours": round(random.uniform(1500, 2000), 2)
}

# Trending fields to simulate realistic values
TRENDING_FIELDS = {
    "fuel_level": {"start": round(random.uniform(70, 90), 2), "min": 5, "max": 100, "delta": -0.3},
    "engine_temp": {"start": round(random.uniform(65, 75), 2), "min": 60, "max": 100, "delta": 0.2}
}
TREND_STATE = {k: v["start"] for k, v in TRENDING_FIELDS.items()}

def sample_param(value):
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return round(random.uniform(*value), 2)
    return value

def apply_trending(field):
    trend = TRENDING_FIELDS[field]
    TREND_STATE[field] += trend["delta"] + random.uniform(-0.1, 0.1)
    TREND_STATE[field] = max(trend["min"], min(trend["max"], TREND_STATE[field]))
    return round(TREND_STATE[field], 2)

def generate_from_phase(phase_params, static):
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "machine_id": MACHINE_ID,
        "operator_id": OPERATOR_ID,
        "terrain": static["terrain"],
        "machine_type": static["machine_type"],
        "task_name": static["task_name"],
        "engine_hours": round(SESSION_STATE["engine_hours"], 2)
    }

    VOLATILE_FIELDS = {
        "speed", "torque", "fuel_level", "engine_temp", "idle_time",
        "vibration_level", "load_weight", "pressure", "fuel_used", "proximity"
    }

    STICKY_FIELDS = {"seatbelt", "geofence_zone", "brake_status", "weather"}

    for field in VOLATILE_FIELDS | STICKY_FIELDS:
        if field in phase_params:
            value = sample_param(phase_params[field])
            if field in STICKY_FIELDS:
                SESSION_STATE[field] = value
            data[field] = value

        elif field in STICKY_FIELDS:
            data[field] = SESSION_STATE.get(field, "unknown")

        elif field in VOLATILE_FIELDS:
            if field in TRENDING_FIELDS:
                data[field] = apply_trending(field)
            elif field == "speed":
                data[field] = round(random.uniform(0, 10), 2)
            elif field == "torque":
                data[field] = round(random.uniform(300, 800), 2)
            elif field == "fuel_used":
                data[field] = round(random.uniform(0.1, 5.0), 2)
            elif field == "engine_temp":
                data[field] = round(random.uniform(60, 100), 2)
            elif field == "idle_time":
                data[field] = random.randint(0, 30)
            elif field == "vibration_level":
                data[field] = round(random.uniform(0.5, 2.5), 2)
            elif field == "load_weight":
                data[field] = round(random.uniform(0, 1000), 2)
            elif field == "pressure":
                data[field] = round(random.uniform(800, 1000), 2)
            elif field == "proximity":
                data[field] = round(random.uniform(0.5, 5.0), 2)

    SESSION_STATE["engine_hours"] += random.uniform(0.005, 0.01)
    data["engine_hours"] = round(SESSION_STATE["engine_hours"], 2)

    return data

def run_task_simulation(task_name="load_truck_flat"):
    task = TASK_SCENARIOS[task_name]
    print(f"[Telemetry] Starting simulation: {task_name}")
    terrain = task["terrain"]
    machine_type = task["machine_type"]

    for phase in task["phases"]:
        print(f"[Phase] {phase['name']}")
        for _ in range(phase["duration"]):
            telemetry = generate_from_phase(
                phase["params"],
                {
                    "terrain": terrain,
                    "machine_type": machine_type,
                    "task_name": task_name
                }
            )
            with open(TELEMETRY_FILE, "w") as f:
                json.dump(telemetry, f, indent=2)
            print(f"[Telemetry] Tick @ {telemetry['timestamp']}")
            time.sleep(DEFAULT_INTERVAL)

    print("[Simulation] Task complete.")

if __name__ == "__main__":
    run_task_simulation()
