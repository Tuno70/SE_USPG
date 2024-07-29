class SistemaExperto:
    def __init__(self):
        self.reglas = []
        self.hechos = []
        self.conclusiones = []

    def agregar_regla(self, condiciones, conclusion):
        self.reglas.append((condiciones, conclusion))

    def agregar_hecho(self, hecho):
        self.hechos.append(hecho)

    def encadenamiento_hacia_adelante(self):
        # Mantener un conjunto de hechos por deducir
        hechos_por_deducir = self.hechos.copy()

        # Mientras haya hechos por deducir
        while hechos_por_deducir:
            # Obtener el primer hecho
            hecho_actual = hechos_por_deducir.pop(0)
            # Revisar cada regla
            for condiciones, conclusion in self.reglas:
                # Si el hecho satisface las condiciones de una regla
                if all(cond in self.hechos for cond in condiciones):
                    # Si la conclusión no está ya en las conclusiones
                    if conclusion not in self.conclusiones:
                        # Agregar la conclusión a las conclusiones
                        self.conclusiones.append(conclusion)
                        # Agregar la conclusión a los hechos por deducir
                        hechos_por_deducir.append(conclusion)

    def mostrar_conclusiones(self):
        print("Conclusiones derivadas:")
        for conclusion in self.conclusiones:
            print(f"- {conclusion}")

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

# Agregar los hechos iniciales
sistema_experto.agregar_hecho("fiebre alta")
sistema_experto.agregar_hecho("dolor muscular")
sistema_experto.agregar_hecho("dificultad para respirar")

# Ejecutar el encadenamiento hacia adelante
sistema_experto.encadenamiento_hacia_adelante()

# Mostrar las conclusiones derivadas
sistema_experto.mostrar_conclusiones()
