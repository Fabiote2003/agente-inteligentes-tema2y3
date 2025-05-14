import numpy as np
import json
from sklearn.model_selection import train_test_split

ALL_SYMPTOMS = [
    "cough", "fever", "fatigue", "loss of taste", "loss of smell",
    "shortness of breath", "headache", "joint pain", "muscle pain", "rash", "sore throat"
]
FEATURES = ALL_SYMPTOMS + ["travel_history", "contact_history"]

def softmax(z):
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def cross_entropy(y_hat, y_true):
    epsilon = 1e-9
    return -np.mean(np.sum(y_true * np.log(y_hat + epsilon), axis=1))

def load_and_prepare_data(filepath="synthetic_patients_3classes.json"):
    with open(filepath, "r") as f:
        data = json.load(f)

    X = []
    y = []

    for patient in data:
        features = patient["features"]
        label = patient["label"]

        x = [features[f] for f in FEATURES]
        X.append(x)

        if label == "dengue":
            y.append([1, 0, 0])
        elif label == "covid":
            y.append([0, 1, 0])
        else:
            y.append([0, 0, 1])

    return np.array(X), np.array(y)

def train_model(x_train, y_train, x_val, y_val, epochs=5500, lr=0.05):
    np.random.seed(0)
    w1 = np.random.randn(x_train.shape[1], 8)
    w2 = np.random.randn(8, 3)

    for epoch in range(epochs):
        z1 = x_train @ w1
        a1 = np.tanh(z1) #como aplicar sidmoid
        z2 = a1 @ w2
        y_hat = softmax(z2)

        loss = cross_entropy(y_hat, y_train)

        #validacion mientras se entrena para detectar overfitting 
        val_a1 = np.tanh(x_val @ w1)
        val_y_hat = softmax(val_a1 @ w2)
        val_loss = cross_entropy(val_y_hat, y_val)

        if epoch % 100 == 0:
            print(f"Epoch {epoch} - Train Loss: {loss:.4f} - Val Loss: {val_loss:.4f}")
        
        # Backpropagation
        # 1. Calcular el gradiente de la pérdida respecto a la pre-activación de la capa de salida (z2)
        dz2 = (y_hat - y_train) / y_train.shape[0]
        # 2. Calcular el gradiente de la pérdida respecto a los pesos de la capa de salida (w2)
        dw2 = a1.T @ dz2
        # 3. Propagar el gradiente de vuelta a la salida de la capa oculta (a1)
        da1 = dz2 @ w2.T
        # 4. Propagar el gradiente a la pre-activación de la capa oculta (z1)
        dz1 = da1 * (1 - np.tanh(z1) ** 2)
        # 5. Calcular el gradiente de la pérdida respecto a los pesos de la capa oculta (w1)
        dw1 = x_train.T @ dz1

        w1 -= lr * dw1
        w2 -= lr * dw2

    print(f"Final loss: {loss:.4f}")

    # Guardar pesos entrenados
    with open("trained_weights.json", "w") as f:
        json.dump({"w1": w1.tolist(), "w2": w2.tolist()}, f)

def evaluate_model(x_val, y_val):
    # Cargar pesos entrenados
    with open("trained_weights.json", "r") as f:
        weights = json.load(f)
    w1 = np.array(weights["w1"])
    w2 = np.array(weights["w2"])

    # Hacer predicciones sobre los datos de validación
    z1 = x_val @ w1
    a1 = np.tanh(z1)
    z2 = a1 @ w2
    y_hat = softmax(z2)

    # Calcular precisión
    correct_predictions = np.sum(np.argmax(y_hat, axis=1) == np.argmax(y_val, axis=1))
    accuracy = correct_predictions / len(y_val)

    print(f"Accuracy on validation set: {accuracy * 100:.2f}%")
    return accuracy

def load_and_train():
    x, y = load_and_prepare_data()
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)
    train_model(x_train, y_train, x_val, y_val)

    # Evaluar el modelo después de entrenarlo
    evaluate_model(x_val, y_val)

def inferir_enfermedad_red_neuronal(symptom_dict, extra_data):
    # Cargar pesos entrenados
    with open("trained_weights.json", "r") as f:
        weights = json.load(f)
    w1 = np.array(weights["w1"])
    w2 = np.array(weights["w2"])

    input_vector = [symptom_dict[symptom] for symptom in ALL_SYMPTOMS]
    input_vector += [int(extra_data["travel_history"]), int(extra_data["contact_history"])]
    x = np.array([input_vector], dtype=float)

    a1 = np.tanh(x @ w1)
    y_hat = softmax(a1 @ w2)

    return float(y_hat[0][0]), float(y_hat[0][1]), float(y_hat[0][2])  # dengue, covid, otra

def get_precautions(disease):
    if disease == "Dengue":
        return "Tomar paracetamol, evitar el ibuprofeno, descansar, hidratarse."
    elif disease == "COVID":
        return "Aislarse, usar barbijo, monitorear síntomas, consultar al médico."
    else:
        return "No se detectaron síntomas relevantes. Mantener hábitos saludables y control médico regular."
