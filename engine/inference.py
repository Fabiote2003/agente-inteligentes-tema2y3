import matplotlib.pyplot as plt
from knowledge_base.symptoms import DESEASES_SYMPTOMNS, EPIDEMIOLOGICAL_DATA, PRECAUTIONS

def define_disease(symptoms):
    scores = {disease: 0 for disease in DESEASES_SYMPTOMNS}
    for symptom in symptoms:
        for disease, data in EPIDEMIOLOGICAL_DATA.items():
            if symptom in data["symptoms"]:
                scores[disease] += 1

    print(scores)

    # 📊 Gráfico de barras
    diseases = list(scores.keys())
    values = list(scores.values())

    plt.figure(figsize=(10, 5))
    plt.bar(diseases, values, color='skyblue')
    plt.title("Puntaje de coincidencia de síntomas por enfermedad")
    plt.xlabel("Enfermedades")
    plt.ylabel("Coincidencias")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return get_precautions(max(scores, key=scores.get))

def get_precautions(disease):
    result = f"\nRecomendamos las siguientes precauciones para {disease}:\n"
    known_precautions = "\n".join([f"- {p}" for p in PRECAUTIONS[disease]])
    result += known_precautions
    print(result)
    setDisease(disease)
    return result


Disease = None  # <- declare it outside any function

def setDisease(disease):
    global Disease
    Disease = disease

def getDisease():
    return Disease