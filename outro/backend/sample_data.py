from typing import Dict, Optional

LOCATION_MAP = {
   "Agartala": {"state": "Tripura", "latitude": 23.8315, "longitude": 91.2868},
    "Ahmedabad": {"state": "Gujarat", "latitude": 23.0225, "longitude": 72.5714},
    "Aizawl": {"state": "Mizoram", "latitude": 23.7271, "longitude": 92.7176},
    "Allahabad (Prayagraj)": {"state": "Uttar Pradesh", "latitude": 25.4358, "longitude": 81.8463},
    "Amritsar": {"state": "Punjab", "latitude": 31.6340, "longitude": 74.8723},

    "Bangalore": {"state": "Karnataka", "latitude": 12.9716, "longitude": 77.5946},
    "Bhopal": {"state": "Madhya Pradesh", "latitude": 23.2599, "longitude": 77.4126},
    "Bhubaneswar": {"state": "Odisha", "latitude": 20.2961, "longitude": 85.8245},
    "Chandigarh": {"state": "Chandigarh", "latitude": 30.7333, "longitude": 76.7794},
    "Chennai": {"state": "Tamil Nadu", "latitude": 13.0827, "longitude": 80.2707},

    "Coimbatore": {"state": "Tamil Nadu", "latitude": 11.0168, "longitude": 76.9558},
    "Delhi": {"state": "Delhi", "latitude": 28.7041, "longitude": 77.1025},
    "Dehradun": {"state": "Uttarakhand", "latitude": 30.3165, "longitude": 78.0322},
    "Guwahati": {"state": "Assam", "latitude": 26.1445, "longitude": 91.7362},

    "Hyderabad": {"state": "Telangana", "latitude": 17.3850, "longitude": 78.4867},
    "Imphal": {"state": "Manipur", "latitude": 24.8170, "longitude": 93.9368},
    "Indore": {"state": "Madhya Pradesh", "latitude": 22.7196, "longitude": 75.8577},

    "Jaipur": {"state": "Rajasthan", "latitude": 26.9124, "longitude": 75.7873},
    "Kanpur": {"state": "Uttar Pradesh", "latitude": 26.4499, "longitude": 80.3319},
    "Kochi": {"state": "Kerala", "latitude": 9.9312, "longitude": 76.2673},
    "Kolkata": {"state": "West Bengal", "latitude": 22.5726, "longitude": 88.3639},

    "Lucknow": {"state": "Uttar Pradesh", "latitude": 26.8467, "longitude": 80.9462},
    "Madurai": {"state": "Tamil Nadu", "latitude": 9.9252, "longitude": 78.1198},
    "Mettur": {"state": "Tamil Nadu", "latitude": 11.7887, "longitude": 77.8300},
    "Mumbai": {"state": "Maharashtra", "latitude": 19.0760, "longitude": 72.8777},

    "Nagpur": {"state": "Maharashtra", "latitude": 21.1458, "longitude": 79.0882},
    "Panaji": {"state": "Goa", "latitude": 15.4909, "longitude": 73.8278},
    "Patna": {"state": "Bihar", "latitude": 25.5941, "longitude": 85.1376},
    "Purna": {"state": "Maharashtra", "latitude": 19.1020, "longitude": 77.4051},
    "Pune": {"state": "Maharashtra", "latitude": 18.5204, "longitude": 73.8567},

    "Raipur": {"state": "Chhattisgarh", "latitude": 21.2514, "longitude": 81.6296},
    "Ranchi": {"state": "Jharkhand", "latitude": 23.3441, "longitude": 85.3096},

    "Shimla": {"state": "Himachal Pradesh", "latitude": 31.1048, "longitude": 77.1734},
    "Srinagar": {"state": "Jammu and Kashmir", "latitude": 34.0837, "longitude": 74.7973},
    "Surat": {"state": "Gujarat", "latitude": 21.1702, "longitude": 72.8311},

    "Ujjini": {"state": "Karnataka", "latitude": 16.8818, "longitude": 76.0049},

    "Varanasi": {"state": "Uttar Pradesh", "latitude": 25.3176, "longitude": 82.9739},
    "Vijayawada": {"state": "Andhra Pradesh", "latitude": 16.5062, "longitude": 80.6480},
    "Visakhapatnam": {"state": "Andhra Pradesh", "latitude": 17.6868, "longitude": 83.2185},
}


def find_latlng(location: str, state: str) -> Optional[Dict[str, float]]:
    key = location.strip().title()
    candidate = LOCATION_MAP.get(key)
    if candidate and candidate["state"].lower() == state.strip().lower():
        return {"latitude": candidate["latitude"], "longitude": candidate["longitude"]}
    return None
