from typing import Optional, Dict

WRIS_REFERENCE = [
    {
        "state": "Karnataka",
        "river": "Krishna",
        "station": "Ujjini",
        "latitude": 16.8818,
        "longitude": 76.0049,
    },
    {
        "state": "Maharashtra",
        "river": "Godavari",
        "station": "Purna",
        "latitude": 19.1020,
        "longitude": 77.4051,
    },
    {
        "state": "Uttar Pradesh",
        "river": "Ganges",
        "station": "Varanasi",
        "latitude": 25.3176,
        "longitude": 82.9739,
    },
    {
        "state": "West Bengal",
        "river": "Hooghly",
        "station": "Kolkata",
        "latitude": 22.5726,
        "longitude": 88.3639,
    },
    {
        "state": "Tamil Nadu",
        "river": "Cauvery",
        "station": "Mettur",
        "latitude": 11.7887,
        "longitude": 77.8300,
    },
]


def find_location(state: str, location: str) -> Optional[Dict[str, float]]:
    state_key = state.strip().lower()
    location_key = location.strip().lower()

    for item in WRIS_REFERENCE:
        if item["state"].lower() == state_key:
            if location_key in item["station"].lower() or location_key in item["river"].lower():
                return {"latitude": item["latitude"], "longitude": item["longitude"]}

    for item in WRIS_REFERENCE:
        if item["state"].lower() == state_key:
            return {"latitude": item["latitude"], "longitude": item["longitude"]}

    return None
