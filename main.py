import tkinter as tk
from tkinter import messagebox
from engine.inference import inferir_enfermedad_bayesiana,plot_probabilities,get_precautions # Importa la nueva función bayesiana

ALL_SYMPTOMS = [
    "cough", "fever", "fatigue", "loss of taste","loss of smell",
    "shortness of breath", "headache", "joint pain", "muscle pain", "rash", "sore throat"
]

def show_result():
    selected_symptoms = [symptom for symptom, var in symptom_vars.items() if var.get()]
    selected_symptom_dict = {symptom: 1 if symptom in selected_symptoms else 0 for symptom in ALL_SYMPTOMS}

    if not selected_symptoms:
        messagebox.showwarning("Atención", "Por favor, seleccioná al menos un síntoma.")
        return

    # Recolectar datos adicionales
    extra_data = {
        #"age": age_var.get(),
        "travel_history": travel_var.get(),  # Este es un booleano
        "contact_history": contact_var.get(),  # Este también es un booleano
        #"season": "summer",
    }

    # Llamamos a la función de inferencia
    p_dengue, p_covid = inferir_enfermedad_bayesiana(selected_symptom_dict, extra_data)

    # Preparamos el diccionario de probabilidades para la gráfica
    probabilities = {
        "Dengue": p_dengue,
        "COVID": p_covid
    }

    # Graficamos las probabilidades
    plot_probabilities(probabilities)

    # Determinamos la enfermedad con la probabilidad más alta
    disease = "Dengue" if p_dengue > p_covid else "COVID"

    # Generamos las recomendaciones
    recomendations = get_precautions(disease)

    # Mostrar mensaje con el resultado
    messagebox.showinfo(
        "Resultado",
        f"Posible enfermedad: {disease.upper()}\n\nRecomendaciones:\n{recomendations}"
    )


# ------------------ UI ------------------ #
root = tk.Tk()
root.title("Detector de enfermedades")
root.geometry("400x500")

tk.Label(root, text="Seleccioná tus síntomas:").pack(pady=10)
symptom_vars = {}

for symptom in ALL_SYMPTOMS:
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, text=symptom.capitalize(), variable=var)
    checkbox.pack(anchor='w')
    symptom_vars[symptom] = var

# Datos adicionales del paciente
tk.Label(root, text="\nEdad del paciente:").pack()
age_var = tk.IntVar(value=35)
tk.Entry(root, textvariable=age_var).pack()

travel_var = tk.BooleanVar()
tk.Checkbutton(root, text="¿Viajó a zona endémica recientemente?", variable=travel_var).pack(anchor='w')

contact_var = tk.BooleanVar()
tk.Checkbutton(root, text="¿Tuvo contacto con un enfermo?", variable=contact_var).pack(anchor='w')

# Botón de diagnóstico
tk.Button(root, text="Diagnosticar", command=show_result).pack(pady=20)

root.mainloop()