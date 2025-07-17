#!/usr/bin/env python3
"""Script to debug exercise creation issues"""

from fastapi.testclient import TestClient
from app.main import app
import json


def test_exercise_creation():
    client = TestClient(app)

    exercise_data = {
        "name": "Bench Press",
        "muscle_group": "CHEST",
        "difficulty": "BEGINNER",
        "sets": 4,
        "reps": 8,
        "comment": "Focus on chest",
        "instructions": "Lie on the bench, grab the bar with medium grip",
        "rest_time_sec": 90,
        "is_compound": True,
        "equipment": "Olympic barbell",
        "exercise_type": "WITH_WEIGHT",
        "with_weight_details": {
            "weight_kg": 80.0,
            "max_weight_kg": 100.0,
            "suggested_increment_kg": 2.5,
        },
    }

    print("Data sent:")
    print(json.dumps(exercise_data, indent=2))

    response = client.post("/api/v1/exercises/", json=exercise_data)

    print(f"\nStatus Code: {response.status_code}")

    try:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
    except:
        print(f"Response text: {response.text}")

    if response.status_code != 201:
        print("\n❌ Error creating exercise!")
        return False
    else:
        print("\n✅ Exercise created successfully!")
        return True


if __name__ == "__main__":
    test_exercise_creation()
