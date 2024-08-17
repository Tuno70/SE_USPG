import tkinter as tk
from tkinter import messagebox

# Clase Persona
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

# Clase RelacionAmistad
class RelacionAmistad:
    def __init__(self):
        self.relaciones_amistad = []

    def agregar_amistad(self, p1, p2):
        self.relaciones_amistad.append((p1, p2))

    def son_amigos(self, p1, p2):
        return (p1, p2) in self.relaciones_amistad or (p2, p1) in self.relaciones_amistad

# Clase Nodo para la red semántica
class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.arcos = []

    def agregar_arco(self, destino, etiqueta_arco):
        self.arcos.append(Arco(self, destino, etiqueta_arco))

# Clase Arco para representar las relaciones entre nodos
class Arco:
    def __init__(self, origen, destino, etiqueta):
        self.origen = origen
        self.destino = destino
        self.etiqueta = etiqueta

    def __str__(self):
        return f"{self.origen.etiqueta} -- {self.etiqueta} --> {self.destino.etiqueta}"

# Clase RedSemantica
class RedSemantica:
    def __init__(self):
        self.nodos = []
        self.recomendaciones = {
            "Gripe": "Paracetamol, Antihistamínicos",
            "Neumonía": "Antibióticos, Reposo",
            "COVID-19": "Antivirales, Oxígeno Suplementario",
            "Resfriado Común": "Analgésicos, Descanso"
        }

    def crear_nodo(self, etiqueta):
        nodo = Nodo(etiqueta)
        self.nodos.append(nodo)
        return nodo

    def obtener_nodo_por_etiqueta(self, etiqueta):
        for nodo in self.nodos:
            if nodo.etiqueta.lower() == etiqueta.lower():
                return nodo
        return None

    def mostrar_red(self):
        for nodo in self.nodos:
            for arco in nodo.arcos:
                print(arco)

    def obtener_recomendacion(self, enfermedad):
        return self.recomendaciones.get(enfermedad, "No hay recomendación disponible")

# Clase SistemaExperto
class SistemaExperto:
    def __init__(self, red_semantica):
        self.red_semantica = red_semantica
        self.hechos = []
        self.conclusiones = []

    def obtener_hechos_y_evaluar(self):
        print("\nIngrese hechos sobre el paciente (por ejemplo, 'Fiebre Alta', 'Dolor Muscular', etc.).")

        while True:
            hecho = input("Ingrese un hecho (o escriba 'evaluar' para obtener un diagnóstico): ").strip().lower()

            if hecho == 'evaluar':
                break

            nodo_hecho = self.red_semantica.obtener_nodo_por_etiqueta(hecho)
            if nodo_hecho:
                self.hechos.append(hecho)
                print(f"Hecho agregado: {hecho}")
            else:
                print("El hecho ingresado no se encuentra en la red semántica.")

        self.evaluar()

        print("\nConclusiones derivadas:")
        for conclusion in self.conclusiones:
            print(f"- {conclusion}: {self.red_semantica.obtener_recomendacion(conclusion)}")

        continuar = input("\n¿Desea ingresar más hechos o salir? (escriba 'continuar' o 'salir'): ").strip().lower()
        if continuar == 'continuar':
            self.hechos.clear()
            self.conclusiones.clear()
            self.obtener_hechos_y_evaluar()
        else:
            print("Gracias por usar el sistema experto. ¡Hasta luego!")

    def evaluar(self):
        for hecho in self.hechos:
            nodo_hecho = self.red_semantica.obtener_nodo_por_etiqueta(hecho)

            if nodo_hecho:
                for arco in nodo_hecho.arcos:
                    if arco.destino.etiqueta not in self.conclusiones:
                        self.conclusiones.append(arco.destino.etiqueta)

# Clase InterfazGrafica
class InterfazGrafica:
    def __init__(self, sistema_experto):
        self.sistema_experto = sistema_experto
        self.root = tk.Tk()
        self.root.title("Sistema Experto de Diagnóstico")
        self.root.geometry("400x300")

        self.label_instrucciones = tk.Label(self.root, text="Ingrese un síntoma y presione 'Agregar'")
        self.label_instrucciones.pack(pady=10)

        self.entry_sintoma = tk.Entry(self.root, width=40)
        self.entry_sintoma.pack(pady=10)

        self.button_agregar = tk.Button(self.root, text="Agregar", command=self.agregar_sintoma)
        self.button_agregar.pack(pady=5)

        self.button_evaluar = tk.Button(self.root, text="Evaluar", command=self.evaluar_sintomas)
        self.button_evaluar.pack(pady=5)

        self.button_salir = tk.Button(self.root, text="Salir", command=self.root.quit)
        self.button_salir.pack(pady=5)

        self.root.mainloop()

    def agregar_sintoma(self):
        sintoma = self.entry_sintoma.get().strip()
        nodo_hecho = self.sistema_experto.red_semantica.obtener_nodo_por_etiqueta(sintoma)

        if nodo_hecho:
            self.sistema_experto.hechos.append(sintoma)
            messagebox.showinfo("Éxito", f"Sintoma '{sintoma}' agregado.")
        else:
            messagebox.showerror("Error", "El síntoma ingresado no se encuentra en la red semántica.")
        self.entry_sintoma.delete(0, tk.END)

    def evaluar_sintomas(self):
        self.sistema_experto.evaluar()
        conclusiones = "\n".join(f"{conclusion}: {self.sistema_experto.red_semantica.obtener_recomendacion(conclusion)}"
                                  for conclusion in self.sistema_experto.conclusiones)

        if conclusiones:
            messagebox.showinfo("Diagnóstico", f"Posibles diagnósticos y recomendaciones:\n{conclusiones}")
        else:
            messagebox.showinfo("Diagnóstico", "No se encontraron diagnósticos basados en los síntomas ingresados.")

        self.sistema_experto.hechos.clear()
        self.sistema_experto.conclusiones.clear()

if __name__ == "__main__":
    # Inicializar la red semántica
    red = RedSemantica()

    # Crear nodos en la red semántica (síntomas y enfermedades)
    fiebre_alta = red.crear_nodo("Fiebre Alta")
    dolor_muscular = red.crear_nodo("Dolor Muscular")
    dificultad_respirar = red.crear_nodo("Dificultad para Respirar")
    tos = red.crear_nodo("Tos")
    dolor_garganta = red.crear_nodo("Dolor de Garganta")
    fatiga = red.crear_nodo("Fatiga")
    perdida_olfato = red.crear_nodo("Pérdida del Olfato")

    gripe = red.crear_nodo("Gripe")
    neumonia = red.crear_nodo("Neumonía")
    covid = red.crear_nodo("COVID-19")
    resfriado = red.crear_nodo("Resfriado Común")

    # Crear relaciones (arcos) entre nodos
    fiebre_alta.agregar_arco(gripe, "es síntoma de")
    dolor_muscular.agregar_arco(gripe, "es síntoma de")
    tos.agregar_arco(gripe, "es síntoma de")
    fiebre_alta.agregar_arco(neumonia, "es síntoma de")
    dificultad_respirar.agregar_arco(neumonia, "es síntoma de")
    tos.agregar_arco(neumonia, "es síntoma de")
    fiebre_alta.agregar_arco(covid, "es síntoma de")
    dificultad_respirar.agregar_arco(covid, "es síntoma de")
    fatiga.agregar_arco(covid, "es síntoma de")
    perdida_olfato.agregar_arco(covid, "es síntoma de")
    dolor_garganta.agregar_arco(resfriado, "es síntoma de")
    tos.agregar_arco(resfriado, "es síntoma de")

    # Crear algunas personas y relaciones de amistad
    juan = Persona("Juan")
    maria = Persona("Maria")
    pedro = Persona("Pedro")

    relaciones = RelacionAmistad()
    relaciones.agregar_amistad(juan, maria)
    relaciones.agregar_amistad(maria, pedro)

    # Comprobaciones de amistad
    print(f"Juan y Maria son amigos? {relaciones.son_amigos(juan, maria)}")
    print(f"Maria y Pedro son amigos? {relaciones.son_amigos(maria, pedro)}")
    print(f"Juan y Pedro son amigos? {relaciones.son_amigos(juan, pedro)}")

    # Inicializar el sistema experto con la red semántica
    sistema_experto = SistemaExperto(red)

    # Lanzar la interfaz gráfica
    InterfazGrafica(sistema_experto)
