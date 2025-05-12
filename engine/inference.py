from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import matplotlib.pyplot as plt
import numpy as np
from knowledge_base.symptoms import DESEASES_SYMPTOMNS, EPIDEMIOLOGICAL_DATA, PRECAUTIONS

def inferir_enfermedad_bayesiana(symptoms, extra_data=None):
    # 1. Definir la estructura de la red bayesiana
    model = DiscreteBayesianNetwork()
    enfermedades = list(DESEASES_SYMPTOMNS.keys())
    sintomas_posibles = set()
    for lista_sintomas in DESEASES_SYMPTOMNS.values():
        sintomas_posibles.update(lista_sintomas)
    sintomas_posibles = list(sintomas_posibles)
    factores_contextuales = ['age', 'travel_history', 'contact_history', 'season']

    for enfermedad in enfermedades:
        model.add_node(enfermedad)
    for sintoma in sintomas_posibles:
        model.add_node(sintoma)
        for enfermedad in enfermedades:
            if sintoma in DESEASES_SYMPTOMNS[enfermedad]:
                model.add_edge(enfermedad, sintoma)
    for factor in factores_contextuales:
        model.add_node(factor)
        if factor == 'travel_history':
            model.add_edge(factor, 'dengue')
        elif factor == 'contact_history':
            model.add_edge(factor, 'covid')
        elif factor == 'age':
            model.add_edge(factor, 'covid')
        elif factor == 'season':
            model.add_edge(factor, 'dengue')

    # 2. Definir las Tablas de Probabilidad Condicional (CPDs)
    # CPD para la edad
    prior_age = np.random.rand(100)
    prior_age /= np.sum(prior_age)
    cpd_age = TabularCPD(variable='age', variable_card=100, values=prior_age.reshape(-1, 1).tolist())
    model.add_cpds(cpd_age)

    # CPD para travel_history (asumiendo probabilidad previa de haber viajado)
    cpd_travel = TabularCPD(variable='travel_history', variable_card=2, values=[[0.2], [0.8]]) # 20% probabilidad de True
    model.add_cpds(cpd_travel)

    # CPD para contact_history (asumiendo probabilidad previa de haber tenido contacto)
    cpd_contact = TabularCPD(variable='contact_history', variable_card=2, values=[[0.1], [0.9]]) # 10% probabilidad de True
    model.add_cpds(cpd_contact)

    # CPD para season (asumiendo probabilidades previas para 'summer' y 'other')
    cpd_season = TabularCPD(variable='season', variable_card=2, values=[[0.3], [0.7]])
    model.add_cpds(cpd_season)

    for enfermedad in enfermedades:
        if model.get_parents(enfermedad):
            evidencia = model.get_parents(enfermedad)
            evidencia_cardinalidad = [2 if factor in ['travel_history', 'contact_history', 'season'] else (100 if factor == 'age' else 2) for factor in evidencia]
            shape = tuple(reversed(evidencia_cardinalidad)) + (2,)
            valores_previos = np.random.rand(*shape)
            valores_previos = valores_previos / np.sum(valores_previos, axis=-1, keepdims=True)
            cpd_data = valores_previos.reshape((-1, 2)).T.tolist()
            cpd = TabularCPD(variable=enfermedad, variable_card=2, values=cpd_data,
                             evidence=evidencia, evidence_card=evidencia_cardinalidad)
            model.add_cpds(cpd)
        else:
            cpd = TabularCPD(variable=enfermedad, variable_card=2, values=[[0.5], [0.5]])
            model.add_cpds(cpd)

    # Definir CPDs para los síntomas considerando múltiples posibles padres (enfermedades)
    for sintoma in sintomas_posibles:
        padres = model.get_parents(sintoma)
        if padres:
            evidencia_cardinalidad = [2] * len(padres) # Cada padre (enfermedad) tiene 2 estados (Sí/No)
            shape = tuple(reversed(evidencia_cardinalidad)) + (2,)
            valores_sintoma = np.random.rand(*shape)
            valores_sintoma = valores_sintoma / np.sum(valores_sintoma, axis=-1, keepdims=True)
            cpd_sintoma_data = valores_sintoma.reshape((-1, 2)).T.tolist()
            cpd_sintoma = TabularCPD(variable=sintoma, variable_card=2, values=cpd_sintoma_data,
                                     evidence=padres, evidence_card=evidencia_cardinalidad)
            model.add_cpds(cpd_sintoma)
        else:
            cpd_sintoma = TabularCPD(variable=sintoma, variable_card=2, values=[[0.1], [0.9]])
            model.add_cpds(cpd_sintoma)

    try:
        model.check_model()
    except Exception as e:
        print(f"Error al verificar el modelo: {e}")
        return None

    infer = VariableElimination(model)
    evidence = {}
    for sintoma in symptoms:
        if sintoma in sintomas_posibles:
            evidence[sintoma] = 1

    if extra_data:
        age = extra_data.get("age")
        travel = extra_data.get("travel_history")
        contact = extra_data.get("contact_history")
        season = extra_data.get("season", "").lower()

        if age is not None:
            evidence['age'] = age
        if travel is not None:
            evidence['travel_history'] = 1 if travel else 0
        if contact is not None:
            evidence['contact_history'] = 1 if contact else 0
        if season:
            evidence['season'] = 1 if season == 'summer' else 0

    # Obtener y mostrar la probabilidad conjunta
    resultados_conjuntos = infer.query(variables=enfermedades, evidence=evidence)
    print("Probabilidades posteriores de las enfermedades:")
    print(resultados_conjuntos)

    probabilidades_enfermedades = {}
    print("\nProbabilidades individuales posteriores:")
    for enfermedad in enfermedades:
        try:
            resultado_marginal = infer.query(variables=[enfermedad], evidence=evidence)
            probabilidades_enfermedades[enfermedad] = resultado_marginal.values[1] if len(resultado_marginal.values) > 1 else resultado_marginal.values[0]
            print(f"  - {enfermedad}: {probabilidades_enfermedades[enfermedad]:.4f}")
        except Exception as e:
            print(f"No se pudo obtener la probabilidad marginal para {enfermedad}: {e}")
            probabilidades_enfermedades[enfermedad] = 0

    predicted_disease = max(probabilidades_enfermedades, key=probabilidades_enfermedades.get)
    print(f"\nEnfermedad predicha (con mayor probabilidad): {predicted_disease}")

    plot_probabilities(probabilidades_enfermedades)

    precautions = get_precautions(predicted_disease)
    return precautions, predicted_disease


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
    if disease in PRECAUTIONS:
        known_precautions = "\n".join([f"- {p}" for p in PRECAUTIONS[disease]])
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
