import tkinter as tk
from tkinter import messagebox, ttk
from engine.inference import naive_bayes_diagnosis, plot_probabilities, get_precautions

ALL_SYMPTOMS = [
    "cough", "fever", "fatigue", "loss of taste", "loss of smell",
    "shortness of breath", "headache", "joint pain", "muscle pain", "rash", "sore throat"
]

# Función principal


def show_result():
    selected_symptoms = [symptom for symptom,
                         var in symptom_vars.items() if var.get()]
    selected_symptom_dict = {
        symptom: 1 if symptom in selected_symptoms else 0 for symptom in ALL_SYMPTOMS}

    if not selected_symptoms:
        messagebox.showwarning(
            "Atención", "Por favor, seleccioná al menos un síntoma.")
        return

    extra_data = {
        "travel_history": travel_var.get(),
        "contact_history": contact_var.get(),
        'season': season_var.get()
    }

    p_dengue, p_covid, p_other = naive_bayes_diagnosis(
        selected_symptom_dict, extra_data)
    p_other = round(max(0.0, 1.0 - (p_dengue + p_covid)), 4)

    probabilities = {
        "Dengue": p_dengue,
        "COVID": p_covid,
        "Otra causa": p_other
    }

    plot_probabilities(probabilities)

    max_prob = max(probabilities.values())
    disease = max(probabilities, key=probabilities.get)
    recomendaciones = get_precautions(disease)

    messagebox.showinfo(
        "Resultado",
        f"Posible causa: {disease.upper()}\n\nRecomendaciones:\n{recomendaciones}"
    )


# ------------------ UI------------------ #
root = tk.Tk()
root.title("Diagnóstico de enfermedades")
root.geometry("500x600")
root.configure(bg="#f0f4f8")

title_label = tk.Label(root, text="Detector de enfermedades", font=(
    "Helvetica", 18, "bold"), bg="#f0f4f8")
title_label.pack(pady=10)

# Frame para los síntomas con scroll
symptom_frame = tk.LabelFrame(
    root, text="Seleccioná tus síntomas", padx=10, pady=10, bg="#ffffff")
symptom_frame.pack(padx=20, pady=10, fill="both", expand=False)

canvas = tk.Canvas(symptom_frame, height=200, bg="#ffffff",
                   bd=0, highlightthickness=0)
scrollbar = ttk.Scrollbar(
    symptom_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#ffffff")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Checkbuttons de síntomas
symptom_vars = {}
for symptom in ALL_SYMPTOMS:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(
        scrollable_frame, text=symptom.capitalize(), variable=var, bg="#ffffff")
    chk.pack(anchor="w")
    symptom_vars[symptom] = var

# Frame para datos adicionales
extra_frame = tk.LabelFrame(
    root, text="Datos adicionales", padx=10, pady=10, bg="#ffffff")
extra_frame.pack(padx=20, pady=10, fill="both", expand=False)

travel_var = tk.BooleanVar()
tk.Checkbutton(extra_frame, text="¿Viajó a zona endémica de Dengue?",
               variable=travel_var, bg="#ffffff").pack(anchor='w')
contact_var = tk.BooleanVar()
tk.Checkbutton(extra_frame, text="¿Tuvo contacto con un enfermo?",
               variable=contact_var, bg="#ffffff").pack(anchor='w')

tk.Label(extra_frame, text="Temporada del año:",
         bg="#ffffff").pack(anchor='w', pady=(10, 0))
season_var = tk.StringVar(value='summer')
season_menu = ttk.Combobox(extra_frame, textvariable=season_var, values=[
                           "summer", "winter"], state="readonly")
season_menu.pack(anchor='w', pady=2)

# Botón de acción
diagnose_btn = tk.Button(
    root,
    text="Diagnosticar",
    command=show_result,
    bg="#4caf50",
    fg="white",
    font=("Helvetica", 12, "bold"),
    relief="flat",
    padx=10,
    pady=5
)
diagnose_btn.pack(pady=20)

root.mainloop()
