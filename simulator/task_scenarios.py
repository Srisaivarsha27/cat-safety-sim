TASK_SCENARIOS = {
    "dig_trench_rocky": {
        "terrain": "rocky",
        "machine_type": "excavator",
        "phases": [
            {
                "name": "approach",
                "duration": 5,
                "params": {
                    "speed": (3, 5),
                    "torque": (400, 600),
                    "seatbelt": "fastened",
                    "geofence_zone": "inside",
                    "fuel_level": (50, 80),
                    "engine_temp": (60, 75),
                    "brake_status": True,
                    "weather": "clear"
                },
            },
            {
                "name": "digging",
                "duration": 10,
                "params": {
                    "speed": (0, 2),
                    "torque": (600, 800),
                    "load_weight": (300, 800),
                    "pressure": (850, 950),
                    "vibration_level": (1.2, 2.5),
                    "seatbelt": "fastened",
                    "idle_time": (5, 15)
                },
            },
            {
                "name": "hazard_proximity_nearby_person",
                "duration": 5,
                "params": {
                    "proximity": (0.5, 1.5),
                    "speed": (0, 1),
                    "seatbelt": "fastened"
                },
            },
            {
                "name": "exit_zone",
                "duration": 5,
                "params": {
                    "speed": (5, 8),
                    "fuel_used": (1, 3),
                    "torque": (300, 500)
                },
            },
        ],
    },

    "load_truck_flat": {
        "terrain": "flat",
        "machine_type": "loader",
        "phases": [
            {
                "name": "drive_to_truck",
                "duration": 5,
                "params": {
                    "speed": (4, 6),
                    "torque": (350, 500),
                    "seatbelt": "fastened",
                    "fuel_level": (60, 90),
                    "engine_temp": (55, 70),
                    "brake_status": True,
                    "weather": "dusty"
                },
            },
            {
                "name": "load_material",
                "duration": 8,
                "params": {
                    "speed": (1, 2),
                    "load_weight": (500, 1000),
                    "pressure": (880, 920),
                    "torque": (500, 700),
                    "vibration_level": (1.0, 2.0),
                    "seatbelt": "fastened"
                },
            },
            {
                "name": "low_fuel_event",
                "duration": 2,
                "params": {
                    "fuel_level": (10, 14),
                    "speed": (2, 4)
                },
            },
        ]
    },

    "navigate_slope_incline": {
        "terrain": "inclined",
        "machine_type": "bulldozer",
        "phases": [
            {
                "name": "climb",
                "duration": 6,
                "params": {
                    "speed": (2, 4),
                    "torque": (700, 850),
                    "engine_temp": (75, 90),
                    "seatbelt": "fastened",
                    "geofence_zone": "inside",
                    "brake_status": False,
                    "weather": "foggy"
                },
            },
            {
                "name": "stall_check",
                "duration": 3,
                "params": {
                    "idle_time": (60, 75),
                    "speed": (0, 0.5),
                    "brake_status": False
                }
            },
            {
                "name": "exit_slope",
                "duration": 4,
                "params": {
                    "speed": (4, 6),
                    "fuel_level": (20, 30),
                    "brake_status": True
                }
            }
        ]
    }
}
