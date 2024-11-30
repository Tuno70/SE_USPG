import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Simulamos algunos datos para entrenar el modelo de Machine Learning
X_train = np.array([
    [1, 2, 0, 2],  # Fiebre leve, Tos moderada, No dolor de cabeza, Fatiga moderada
    [2, 0, 1, 1],  # Fiebre moderada, No Tos, Dolor de cabeza leve, Fatiga leve
    [0, 3, 2, 3],  # No Fiebre, Tos grave, Dolor de cabeza moderado, Fatiga grave
    [1, 2, 1, 2],  # Fiebre leve, Tos moderada, Dolor de cabeza leve, Fatiga moderada
    [0, 0, 0, 0],  # Ningún síntoma
])

y_train = np.array(["Resfriado", "Gripe", "COVID-19", "Resfriado", "Gripe"])  # Enfermedades: Resfriado, Gripe, COVID-19

# Entrenamos el modelo KNN
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Función para predecir la enfermedad basándose en los síntomas
def diagnosticar():
    try:
        fiebre = combo_fiebre.get()
        tos = combo_tos.get()
        dolor_cabeza = combo_dolor_cabeza.get()
        fatiga = combo_fatiga.get()

        # Convertimos los valores seleccionados en índices para hacer la predicción
        sintomas_map = {"Ninguno": 0, "Leve": 1, "Moderado": 2, "Grave": 3}
        
        # Aseguramos que las selecciones sean válidas
        if fiebre == "Seleccionar" or tos == "Seleccionar" or dolor_cabeza == "Seleccionar" or fatiga == "Seleccionar":
            messagebox.showerror("Error", "Por favor, seleccione todos los síntomas")
            return
        
        fiebre = sintomas_map[fiebre]
        tos = sintomas_map[tos]
        dolor_cabeza = sintomas_map[dolor_cabeza]
        fatiga = sintomas_map[fatiga]
        
        # Hacer la predicción usando el modelo entrenado
        prediction = model.predict([[fiebre, tos, dolor_cabeza, fatiga]])
        
        # Mostrar el diagnóstico basado en la predicción
        messagebox.showinfo("Diagnóstico", f"Probable enfermedad: {prediction[0]}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al hacer el diagnóstico: {e}")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sistema Experto Médico")
root.geometry("400x400")

# Crear el título
label = tk.Label(root, text="Seleccione los síntomas:")
label.pack(pady=10)

# Crear los combo boxes para elegir la intensidad de los síntomas
label_fiebre = tk.Label(root, text="Fiebre:")
label_fiebre.pack()
combo_fiebre = ttk.Combobox(root, values=["Seleccionar", "Ninguno", "Leve", "Moderado", "Grave"])
combo_fiebre.set("Seleccionar")
combo_fiebre.pack()

label_tos = tk.Label(root, text="Tos:")
label_tos.pack()
combo_tos = ttk.Combobox(root, values=["Seleccionar", "Ninguno", "Leve", "Moderado", "Grave"])
combo_tos.set("Seleccionar")
combo_tos.pack()

label_dolor_cabeza = tk.Label(root, text="Dolor de cabeza:")
label_dolor_cabeza.pack()
combo_dolor_cabeza = ttk.Combobox(root, values=["Seleccionar", "Ninguno", "Leve", "Moderado", "Grave"])
combo_dolor_cabeza.set("Seleccionar")
combo_dolor_cabeza.pack()

label_fatiga = tk.Label(root, text="Fatiga:")
label_fatiga.pack()
combo_fatiga = ttk.Combobox(root, values=["Seleccionar", "Ninguno", "Leve", "Moderado", "Grave"])
combo_fatiga.set("Seleccionar")
combo_fatiga.pack()

# Botón para realizar el diagnóstico
button_diagnosticar = tk.Button(root, text="Diagnosticar", command=diagnosticar)
button_diagnosticar.pack(pady=20)

# Botón para limpiar los campos
def limpiar():
    combo_fiebre.set("Seleccionar")
    combo_tos.set("Seleccionar")
    combo_dolor_cabeza.set("Seleccionar")
    combo_fatiga.set("Seleccionar")

button_limpiar = tk.Button(root, text="Limpiar", command=limpiar)
button_limpiar.pack()

# Iniciar la interfaz gráfica
root.mainloop()
