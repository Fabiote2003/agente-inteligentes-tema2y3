from knowledge_base.symptoms import DESEASES_SYMPTOMNS, EPIDEMIOLOGICAL_DATA, PRECAUTIONS

def define_disease(symptoms):
    scores = {desease: 0 for desease in DESEASES_SYMPTOMNS}
    for symptom in symptoms:
        for disease, data in EPIDEMIOLOGICAL_DATA.items():
            if symptom in data["symptoms"]:
                scores[disease] += 1
    print(scores)
    return get_precautions(max(scores, key=scores.get))

def get_precautions(disease):
    print(f"We recommend the following precautions for {disease}:")
    known_precautions = "\n".join([f"- {p}" for p in PRECAUTIONS[disease]])
    print(known_precautions)