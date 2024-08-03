class SistemaExperto:
    def __init__(self):
        self.reglas = []
        self.hechos = []
        self.conclusiones = []

    def agregar_regla(self, condiciones, conclusion):
        """Agrega una regla al sistema experto"""
        self.reglas.append((condiciones, conclusion))

    def agregar_hecho(self, hecho):
        """Agrega un hecho al sistema experto"""
        self.hechos.append(hecho)

    def encadenamiento_hacia_adelante(self):
        """Aplica el encadenamiento hacia adelante para derivar conclusiones"""
        hechos_por_deducir = self.hechos.copy()

        while hechos_por_deducir:
            hecho_actual = hechos_por_deducir.pop(0)
            for condiciones, conclusion in self.reglas:
                if all(cond in self.hechos for cond in condiciones):
                    if conclusion not in self.conclusiones:
                        self.conclusiones.append(conclusion)
                        hechos_por_deducir.append(conclusion)

    def mostrar_conclusiones(self):
        """Muestra las conclusiones derivadas"""
        if self.conclusiones:
            print("\nConclusiones derivadas:")
            for conclusion in self.conclusiones:
                print(f"- {conclusion}")
        else:
            print("\nNo se derivaron conclusiones con los hechos proporcionados.")

    def restablecer(self):
        """Restablece las conclusiones y hechos para una nueva evaluación"""
        self.conclusiones.clear()
        self.hechos.clear()

# Inicializar el sistema experto
sistema_experto = SistemaExperto()

# Definir las reglas del sistema experto
sistema_experto.agregar_regla(
    condiciones=["fiebre alta", "dolor muscular"],
    conclusion="el paciente podría tener gripe"
)

sistema_experto.agregar_regla(
    condiciones=["congestión nasal", "estornudos"],
    conclusion="el paciente podría tener un resfriado común"
)

sistema_experto.agregar_regla(
    condiciones=["tos persistente", "mucosidad"],
    conclusion="el paciente podría tener bronquitis"
)

sistema_experto.agregar_regla(
    condiciones=["fiebre alta", "dificultad para respirar"],
    conclusion="el paciente podría tener neumonía"
)

sistema_experto.agregar_regla(
    condiciones=["dificultad severa para respirar"],
    conclusion="el paciente debe buscar atención médica inmediata"
)

# Función para interactuar con el usuario y obtener hechos
def obtener_hechos():
    print("\nIngrese hechos sobre el paciente (por ejemplo, 'fiebre alta', 'tos persistente', etc.).")
    while True:
        hecho = input("Ingrese un hecho (o escriba 'evaluar' para obtener un diagnóstico): ").strip().lower()
        if hecho == 'evaluar':
            break
        elif hecho:
            sistema_experto.agregar_hecho(hecho)
            print(f"Hecho agregado: {hecho}")
        else:
            print("Por favor, ingrese un hecho válido.")

# Ciclo principal para la interacción del usuario
while True:
    # Obtener hechos del usuario
    obtener_hechos()

    # Ejecutar el encadenamiento hacia adelante
    sistema_experto.encadenamiento_hacia_adelante()

    # Mostrar las conclusiones derivadas
    sistema_experto.mostrar_conclusiones()

    # Preguntar al usuario si desea continuar o salir
    continuar = input("\n¿Desea ingresar más hechos o salir? (escriba 'continuar' o 'salir'): ").strip().lower()
    if continuar == 'salir':
        print("Gracias por usar el sistema experto. ¡Hasta luego!")
        break
    elif continuar == 'continuar':
        sistema_experto.restablecer()
    else:
        print("Opción no válida. El programa continuará para ingresar más hechos.")
        sistema_experto.restablecer()
