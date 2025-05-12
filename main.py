import tkinter as tk
from tkinter import messagebox
from engine.inference import inferir_enfermedad_bayesiana # Importa la nueva función bayesiana

ALL_SYMPTOMS = [
    "cough", "fever", "fatigue", "loss of taste or smell",
    "shortness of breath", "headache", "joint pain", "muscle pain", "rash", "sore throat"
]

def show_result():
    selected_symptoms = [symptom for symptom, var in symptom_vars.items() if var.get()]

    if not selected_symptoms:
        messagebox.showwarning("Atención", "Por favor, seleccioná al menos un síntoma.")
        return

    # Recolectar datos adicionales
    extra_data = {
        "age": age_var.get(),
        "travel_history": travel_var.get(),
        "contact_history": contact_var.get(),
        "season": "summer",
    }

    # Enviar a tu motor de inferencia bayesiano
    recomendations, predicted_disease = inferir_enfermedad_bayesiana(selected_symptoms, extra_data)

    messagebox.showinfo("Resultado", f"Posible enfermedad: {predicted_disease.upper()}\n\nRecomendaciones:\n{recomendations}")

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