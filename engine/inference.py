from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import matplotlib.pyplot as plt
import numpy as np
from knowledge_base.symptoms import DESEASES_SYMPTOMNS, EPIDEMIOLOGICAL_DATA, PRECAUTIONS
import itertools
np.random.seed(42)  # Cualquier número fijo sirve

def symptom_cpd(symptom_name, prob_if_disease, prob_if_no_disease, parent):
    return TabularCPD(
        variable=symptom_name, variable_card=2,
        values=[
            [1 - prob_if_disease, 1 - prob_if_no_disease],
            [prob_if_disease, prob_if_no_disease]
        ],
        evidence=[parent],
        evidence_card=[2]
    )


def symptom_cpd(symptom_name, probs_given_disease, parent='disease'):
    """
    probs_given_disease: dict mapping disease value to P(symptom=True | disease)
    """
    # Asumimos disease_card = 2 (0: dengue, 1: covid)
    prob_dengue = probs_given_disease.get('dengue', 0.5)
    prob_covid = probs_given_disease.get('covid', 0.5)
    return TabularCPD(
        variable=symptom_name, variable_card=2,
        values=[
            [1 - prob_dengue, 1 - prob_covid],  # symptom = 0
            [prob_dengue, prob_covid]           # symptom = 1
        ],
        evidence=[parent],
        evidence_card=[2]
    )

def naive_bayes_diagnosis(symptoms_dict):
    # Definir modelo naive bayes: disease -> all symptoms
    model = DiscreteBayesianNetwork([
        ('disease', 'fever'),
        ('disease', 'cough'),
        ('disease', 'fatigue'),
        ('disease', 'loss of taste'),
        ('disease', 'loss of smell'),
        ('disease', 'shortness of breath'),
        ('disease', 'sore throat'),
        ('disease', 'rash'),
        ('disease', 'headache'),
        ('disease', 'joint pain'),
        ('disease', 'muscle pain')
    ])

    # CPD de disease (naive bayes asume P(disease))
    cpd_disease = TabularCPD(
        variable='disease', variable_card=2,
        values=[[0.5], [0.5]]  # 0: dengue, 1: covid
    )

    # CPDs de síntomas condicionales a disease
    cpds = [
        symptom_cpd('fever', {'dengue': 0.05, 'covid': 0.95}),
        symptom_cpd('cough', {'dengue': 0.1, 'covid': 0.9}),
        symptom_cpd('fatigue', {'dengue': 0.15, 'covid': 0.85}),
        symptom_cpd('loss of taste', {'dengue': 0.05, 'covid': 0.95}),
        symptom_cpd('loss of smell', {'dengue': 0.05, 'covid': 0.95}),
        symptom_cpd('shortness of breath', {'dengue': 0.15, 'covid': 0.85}),
        symptom_cpd('sore throat', {'dengue': 0.2, 'covid': 0.8}),
        symptom_cpd('rash', {'dengue': 0.85, 'covid': 0.1}),
        symptom_cpd('headache', {'dengue': 0.75, 'covid': 0.2}),
        symptom_cpd('joint pain', {'dengue': 0.8, 'covid': 0.1}),
        symptom_cpd('muscle pain', {'dengue': 0.75, 'covid': 0.3})
    ]

    # Agregar CPDspip3.10 install pgmpy
    model.add_cpds(cpd_disease, *cpds)

    assert model.check_model()

    # Construir evidencia
    evidencia = {}
    for symptom in symptoms_dict:
        evidencia[symptom] = int(symptoms_dict[symptom])  # 1 si presente, 0 si no

    # Inferencia
    infer = VariableElimination(model)
    result = infer.query(variables=['disease'], evidence=evidencia)

    # Resultado
    p_dengue = result.values[0]
    p_covid = result.values[1]

    print(f"Probabilidad de dengue: {p_dengue:.4f}")
    print(f"Probabilidad de covid: {p_covid:.4f}")
    return round(p_dengue, 4), round(p_covid, 4)


def plot_probabilities(probabilities):
    diseases = list(probabilities.keys())
    values = list(probabilities.values())

    plt.figure(figsize=(10, 5))
    plt.bar(diseases, values, color='lightcoral')
    plt.title("Probabilidad posterior de cada enfermedad")
    plt.xlabel("Enfermedades")
    plt.ylabel("Probabilidad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def get_precautions(disease):
    result = f"\nRecomendamos las siguientes precauciones para {disease.upper()}:\n"
    if disease.lower() in PRECAUTIONS:
        known_precautions = "\n".join([f"- {p}" for p in PRECAUTIONS[disease.lower()]])
        result += known_precautions
    else:
        result += "No se encontraron precauciones específicas para esta enfermedad."
    print(result)
    return result
def setDisease(disease):
    global Disease
    Disease = disease

def getDisease():
    return Disease
