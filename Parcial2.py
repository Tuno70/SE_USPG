import sqlite3
from tkinter import *
from tkinter import messagebox

# Conexión a la base de datos SQLite
def conectar_bd():
    conn = sqlite3.connect('base_conocimiento.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reglas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        regla TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS hechos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hecho TEXT)''')
    conn.commit()
    return conn, cursor

# Precargar base de datos con síntomas y reglas
def precargar_datos():
    conn, cursor = conectar_bd()

    # Precargar síntomas si no existen
    sintomas_iniciales = ["tos", "fiebre", "dolor de cabeza", "náuseas"]
    for sintoma in sintomas_iniciales:
        cursor.execute('SELECT * FROM hechos WHERE hecho = ?', (sintoma,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO hechos (hecho) VALUES (?)', (sintoma,))

    # Precargar reglas si no existen
    reglas_iniciales = [
        "tos, fiebre -> gripe",
        "dolor de cabeza, fiebre -> migraña",
        "náuseas, fiebre -> infección estomacal"
    ]
    for regla in reglas_iniciales:
        cursor.execute('SELECT * FROM reglas WHERE regla = ?', (regla,))
        if not cursor.fetchone():
            cursor.execute('INSERT INTO reglas (regla) VALUES (?)', (regla,))

    conn.commit()
    conn.close()

# Insertar nuevas reglas en la base de conocimiento
def agregar_regla(regla):
    conn, cursor = conectar_bd()
    cursor.execute('INSERT INTO reglas (regla) VALUES (?)', (regla,))
    conn.commit()
    conn.close()

# Insertar nuevos hechos en la base de conocimiento
def agregar_hecho(hecho):
    conn, cursor = conectar_bd()
    cursor.execute('INSERT INTO hechos (hecho) VALUES (?)', (hecho,))
    conn.commit()
    conn.close()

# Obtener las reglas desde la base de datos
def obtener_reglas():
    conn, cursor = conectar_bd()
    cursor.execute('SELECT * FROM reglas')
    reglas = cursor.fetchall()
    conn.close()
    return reglas

# Obtener los hechos (síntomas) desde la base de datos
def obtener_hechos():
    conn, cursor = conectar_bd()
    cursor.execute('SELECT hecho FROM hechos')
    hechos = [hecho[0] for hecho in cursor.fetchall()]
    conn.close()
    return hechos

# Sistema experto - Encadenamiento hacia adelante
def diagnosticar(hechos_usuario):
    reglas = obtener_reglas()
    for regla_id, regla in reglas:
        if all(hecho in hechos_usuario for hecho in regla.split(" -> ")[0].split(", ")):
            return regla.split(" -> ")[1]
    return "No se encontró un diagnóstico para los hechos ingresados."

# Interfaz gráfica mejorada
def iniciar_interfaz():
    root = Tk()
    root.title("Sistema Experto - Diagnóstico Médico")
    precargar_datos()

    Label(root, text="Sistema Experto de Diagnóstico Médico", font=("Arial", 16)).pack(pady=10)

    # Mostrar reglas actuales
    Label(root, text="Reglas disponibles:").pack(pady=5)
    reglas_listbox = Listbox(root, width=100)
    reglas_listbox.pack(pady=5)
    reglas = obtener_reglas()
    for regla_id, regla in reglas:
        reglas_listbox.insert(END, f"{regla}")

    Label(root, text="Seleccione los síntomas:").pack(pady=5)

    sintomas_disponibles = obtener_hechos()
    sintomas_seleccionados = []

    # Crear menú desplegable para seleccionar síntomas
    def agregar_sintoma():
        sintoma = sintomas_var.get()
        if sintoma and sintoma not in sintomas_seleccionados:
            sintomas_seleccionados.append(sintoma)
            sintomas_seleccionados_listbox.insert(END, sintoma)
        else:
            messagebox.showwarning("Advertencia", "El síntoma ya fue seleccionado o no es válido.")

    sintomas_var = StringVar(root)
    sintomas_var.set("Selecciona un síntoma")
    sintomas_menu = OptionMenu(root, sintomas_var, *sintomas_disponibles)
    sintomas_menu.pack(pady=5)

    Button(root, text="Agregar Síntoma", command=agregar_sintoma).pack(pady=5)

    Label(root, text="Síntomas seleccionados:").pack(pady=5)
    sintomas_seleccionados_listbox = Listbox(root, width=50)
    sintomas_seleccionados_listbox.pack(pady=5)

    # Función para diagnosticar
    def diagnosticar_enfermedad():
        if sintomas_seleccionados:
            diagnostico = diagnosticar(sintomas_seleccionados)
            messagebox.showinfo("Diagnóstico", f"Resultado: {diagnostico}")
        else:
            messagebox.showwarning("Error", "Debe seleccionar al menos un síntoma para diagnosticar.")

    Button(root, text="Diagnosticar", command=diagnosticar_enfermedad).pack(pady=10)

    # Botón para limpiar síntomas seleccionados
    def limpiar_sintomas():
        sintomas_seleccionados.clear()
        sintomas_seleccionados_listbox.delete(0, END)
        messagebox.showinfo("Limpieza", "Los síntomas seleccionados han sido eliminados.")

    Button(root, text="Limpiar Síntomas", command=limpiar_sintomas).pack(pady=5)

    # Función para agregar nuevos síntomas
    def agregar_nuevo_sintoma():
        nuevo_sintoma = nuevo_sintoma_entry.get()
        if nuevo_sintoma:
            agregar_hecho(nuevo_sintoma)
            sintomas_menu['menu'].add_command(label=nuevo_sintoma, command=lambda v=nuevo_sintoma: sintomas_var.set(v))
            messagebox.showinfo("Síntoma agregado", f"Nuevo síntoma '{nuevo_sintoma}' agregado")
            nuevo_sintoma_entry.delete(0, END)
        else:
            messagebox.showwarning("Error", "Debe ingresar un síntoma válido")

    # Sección para agregar nuevos síntomas
    Label(root, text="Agregar nuevo síntoma:").pack(pady=10)
    nuevo_sintoma_entry = Entry(root, width=50)
    nuevo_sintoma_entry.pack(pady=5)

    Button(root, text="Agregar Síntoma", command=agregar_nuevo_sintoma).pack(pady=5)

    # Sección para agregar nuevas reglas
    Label(root, text="Agregar nueva regla (formato: sintoma1, sintoma2 -> diagnostico):").pack(pady=10)
    regla_entry = Entry(root, width=50)
    regla_entry.pack(pady=5)

    def agregar_nueva_regla():
        nueva_regla = regla_entry.get()
        if nueva_regla:
            agregar_regla(nueva_regla)
            messagebox.showinfo("Regla agregada", f"Regla '{nueva_regla}' agregada")
            reglas_listbox.insert(END, nueva_regla)
        else:
            messagebox.showwarning("Error", "Debe ingresar una regla válida")

    Button(root, text="Agregar Regla", command=agregar_nueva_regla).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
