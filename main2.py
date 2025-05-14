import tkinter as tk
from tkinter import messagebox
from learner import inferir_enfermedad_red_neuronal, get_precautions

ALL_SYMPTOMS = [
    "cough", "fever", "fatigue", "loss of taste", "loss of smell",
    "shortness of breath", "headache", "joint pain", "muscle pain", "rash", "sore throat"
]
from learner import load_and_train
load_and_train()
def show_result():
    selected_symptom_dict = {symptom: var.get() for symptom, var in symptom_vars.items()}
    if not any(selected_symptom_dict.values()):
        messagebox.showwarning("Atención", "Por favor, seleccioná al menos un síntoma.")
        return

    extra_data = {
        "travel_history": travel_var.get(),
        "contact_history": contact_var.get()
    }
    
    # Ahora devuelve 3 probabilidades
    p_dengue, p_covid, p_otra = inferir_enfermedad_red_neuronal(selected_symptom_dict, extra_data)

    probs = {
        "Dengue": p_dengue,
        "COVID": p_covid,
        "Otra": p_otra
    }

    disease = max(probs, key=probs.get)
    recomendaciones = get_precautions(disease)

    messagebox.showinfo(
        "Resultado",
        f"Probabilidad de Dengue: {p_dengue:.2f}\n"
        f"Probabilidad de COVID: {p_covid:.2f}\n"
        f"Probabilidad de Otra: {p_otra:.2f}\n\n"
        f"Posible enfermedad: {disease.upper()}\n\nRecomendaciones:\n{recomendaciones}"
    )


# ------------------ UI ------------------ #
root = tk.Tk()
root.title("Detector de Enfermedades")
root.geometry("400x600")

tk.Label(root, text="Seleccioná tus síntomas:").pack(pady=10)
symptom_vars = {}

for symptom in ALL_SYMPTOMS:
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, text=symptom.capitalize(), variable=var)
    checkbox.pack(anchor='w')
    symptom_vars[symptom] = var

# Datos adicionales del paciente
tk.Label(root, text="\nEdad del paciente (no usado):").pack()
age_var = tk.IntVar(value=35)
tk.Entry(root, textvariable=age_var).pack()

travel_var = tk.BooleanVar()
tk.Checkbutton(root, text="¿Viajó a zona endémica recientemente?", variable=travel_var).pack(anchor='w')

contact_var = tk.BooleanVar()
tk.Checkbutton(root, text="¿Tuvo contacto con un enfermo?", variable=contact_var).pack(anchor='w')

# Botón de diagnóstico
tk.Button(root, text="Diagnosticar", command=show_result).pack(pady=20)

root.mainloop()
