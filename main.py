import tkinter as tk
from tkinter import messagebox
from engine.inference import define_disease,getDisease

# Diccionario de síntomas posibles (puede extenderse)
ALL_SYMPTOMS = [
    "cough",
    "fever",
    "fatigue",
    "loss of taste or smell",
    "shortness of breath",
    "headache",
    "joint pain",
    "muscle pain",
    "rash",
]

def show_result():
    selected_symptoms = [symptom for symptom, var in symptom_vars.items() if var.get()]
    if not selected_symptoms:
        messagebox.showwarning("Atención", "Por favor, seleccioná al menos un síntoma.")
        return
    recomendations=define_disease(selected_symptoms)
    result = getDisease()
    
    messagebox.showinfo("Resultado", f"Posible enfermedad: {result} \n {recomendations}")

# Interfaz
root = tk.Tk()
root.title("Detector de enfermedades")
root.geometry("300x300") 
tk.Label(root, text="Seleccioná tus síntomas:").pack(pady=10)

symptom_vars = {}

# Crear los checkboxes
for symptom in ALL_SYMPTOMS:
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(root, text=symptom.capitalize(), variable=var)
    checkbox.pack(anchor='w')
    symptom_vars[symptom] = var

# Botón para enviar
tk.Button(root, text="Diagnosticar", command=show_result).pack(pady=20)

root.mainloop()
