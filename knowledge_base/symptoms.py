DESEASES_SYMPTOMNS = {
    "covid": [
        "cough",
        "fever",
        "fatigue",
        "loss of taste or smell",
        "shortness of breath",
        "sore throat",
    ],
    "dengue": [
        "fever",
        "headache",
        "joint pain",
        "muscle pain",
        "rash",
        "sore throat",
    ]
}

EPIDEMIOLOGICAL_DATA = {
    "covid": {
        "cases": 100000,
        "deaths": 10000,
        "recovery_rate": 0.95,
        "transmission_rate": 0.5,
        "symptoms": DESEASES_SYMPTOMNS["covid"],
        "regional_activity": "active",  # circulando activamente
        "seasonal_risk": {
            "summer": "medium",
            "winter": "high"
        }
    },
    "dengue": {
        "cases": 100000,
        "deaths": 10000,
        "recovery_rate": 0.95,
        "transmission_rate": 0.5,
        "symptoms": DESEASES_SYMPTOMNS["dengue"],
        "regional_activity": "outbreak",  # brote activo
        "seasonal_risk": {
            "summer": "high",
            "winter": "low"
        }
    }
}

PRECAUTIONS = {
    "covid": [
        "wear a mask",
        "wash your hands",
        "social distance",
        "stay home if you are sick",
    ],
    "dengue": [
        "wear long sleeves",
        "use mosquito repellent",
        "sleep under mosquito net",
        "get vaccinated",
    ],
    "another_cause": ["consult a doctor",],
}

if __name__ != "__main__":
    __all__ = ["DESEASES_SYMPTOMNS","EPIDEMIOLOGICAL_DATA", "PRECAUTIONS"]