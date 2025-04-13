import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
from transformers import pipeline


DESEASES_SYMPTOMNS = {
    "covid": [
        "cough",
        "fever",
        "fatigue",
        "loss of taste or smell",
        "shortness of breath",
    ],
    "dengue": [
        "fever",
        "headache",
        "joint pain",
        "muscle pain",
        "rash",
    ]
}

EPIDEMIOLOGICAL_DATA = {
    "covid": {
        "cases": 100000,
        "deaths": 10000,
        "recovery_rate": 0.95,
        "transmission_rate": 0.5,
        "symptoms": DESEASES_SYMPTOMNS["covid"],
    },
    "dengue": {
        "cases": 100000,
        "deaths": 10000,
        "recovery_rate": 0.95,
        "transmission_rate": 0.5,
        "symptoms": DESEASES_SYMPTOMNS["dengue"],
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
    ]
}

if __name__ != "__main__":
    __all__ = ["DESEASES_SYMPTOMNS", "EPIDEMIOLOGICAL_DATA", "PRECAUTIONS"]