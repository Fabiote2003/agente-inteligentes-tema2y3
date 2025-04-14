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
    __all__ = ["DESEASES_SYMPTOMNS", "PRECAUTIONS"]