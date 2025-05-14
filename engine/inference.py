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


def symptom_cpd(symptom, prob_dict):
    """
    Crea un CPD para un síntoma binario dado tres posibles estados de "disease":
    'dengue', 'covid', 'other'.
    prob_dict debe mapear cada etiqueta de enfermedad a P(symptom=1 | disease).
    Se asume ordering disease=[dengue, covid, other].
    """
    p_d = prob_dict.get('dengue', 0.05)
    p_c = prob_dict.get('covid', 0.05)
    p_o = prob_dict.get('other', 0.05)
    # filas: symptom=0, symptom=1; columnas: dengue, covid, other
    return TabularCPD(
        variable=symptom,
        variable_card=2,
        values=[
            [1 - p_d, 1 - p_c, 1 - p_o],
            [p_d,      p_c,      p_o]
        ],
        evidence=['disease'],
        evidence_card=[3]
    )


def naive_bayes_diagnosis(symptoms_dict, extra_data):
    """
    Diagnosticar entre Dengue, COVID-19 u Otra causa usando Naive Bayes,
    con priors dinámicos y CPDs para un modelo de 3 estados.
    symptoms_dict: dict sintoma->0/1
    extra_data: {'travel_history', 'contact_history', 'season'}
    Devuelve P(dengue), P(covid), P(other).
    """
    # 1. Priori dinámico para dengue y covid
    prior_d = 0.5 + 0.1
    if extra_data.get('travel_history'):
        prior_d += 0.15
    if extra_data.get('contact_history'):
        prior_d += 0.2
    if extra_data.get('season') == 'summer':
        prior_d += 0.1
    elif extra_data.get('season') == 'winter':
        prior_d -= 0.1
    prior_d = np.clip(prior_d, 0.01, 0.99)

    prior_c = 1 - prior_d  # temporal, antes de asignar other
    # asignar una fracción al "other"
    prior_o = 0.3 * prior_c
    prior_c = prior_c - prior_o
    prior_o = np.clip(prior_o, 0.01, 0.98)
    prior_c = np.clip(prior_c, 0.01, 0.98)

    # 2. Construir red bayesiana
    model = DiscreteBayesianNetwork([('disease', s) for s in (
        'fever', 'cough', 'fatigue', 'loss of taste', 'loss of smell',
        'shortness of breath', 'sore throat', 'rash', 'headache',
        'joint pain', 'muscle pain', 'travel_history', 'contact_history'
    )])

    # 3. Prior de disease con 3 estados
    cpd_disease = TabularCPD(
        variable='disease', variable_card=3,
        values=[[prior_d], [prior_c], [prior_o]]
    )

    # 4. CPDs condicionales
    cpds = [
        symptom_cpd('fever',             {
                    'dengue': 0.05, 'covid': 0.95, 'other': 0.1}),
        symptom_cpd('cough',             {
                    'dengue': 0.1,  'covid': 0.9,  'other': 0.1}),
        symptom_cpd('fatigue',           {
                    'dengue': 0.15, 'covid': 0.85, 'other': 0.1}),
        symptom_cpd('loss of taste',     {
                    'dengue': 0.05, 'covid': 0.95, 'other': 0.01}),
        symptom_cpd('loss of smell',     {
                    'dengue': 0.05, 'covid': 0.95, 'other': 0.01}),
        symptom_cpd('shortness of breath', {
                    'dengue': 0.15, 'covid': 0.85, 'other': 0.05}),
        symptom_cpd('sore throat',       {
                    'dengue': 0.2,  'covid': 0.8,  'other': 0.1}),
        symptom_cpd('rash',              {
                    'dengue': 0.85, 'covid': 0.1,  'other': 0.02}),
        symptom_cpd('headache',          {
                    'dengue': 0.75, 'covid': 0.2,  'other': 0.1}),
        symptom_cpd('joint pain',        {
                    'dengue': 0.8,  'covid': 0.1,  'other': 0.1}),
        symptom_cpd('muscle pain',       {
                    'dengue': 0.75, 'covid': 0.3,  'other': 0.2}),
        symptom_cpd('travel_history',    {
                    'dengue': 0.7,  'covid': 0.3,  'other': 0.05}),
        symptom_cpd('contact_history',   {
                    'dengue': 0.8,  'covid': 0.2,  'other': 0.05}),
    ]

    # 5. Agregar CPDs
    model.add_cpds(cpd_disease, *cpds)
    assert model.check_model(), "Modelo no válido"

    # 6. Construir evidencia
    evidence = {s: int(symptoms_dict.get(s, 0)) for s in symptoms_dict}
    evidence['travel_history'] = int(
        bool(extra_data.get('travel_history', False)))
    evidence['contact_history'] = int(
        bool(extra_data.get('contact_history', False)))

    # 7. Inferencia
    infer = VariableElimination(model)
    result = infer.query(['disease'], evidence=evidence)

    p_d, p_c, p_o = result.values
    print(f"P(dengue)={p_d:.4f}, P(covid)={p_c:.4f}, P(other)={p_o:.4f}")

    return round(p_d, 4), round(p_c, 4), round(p_o, 4)


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
