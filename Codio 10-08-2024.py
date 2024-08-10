class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.arcos = []

    def agregar_arco(self, destino, etiqueta_arco):
        self.arcos.append(Arco(self, destino, etiqueta_arco))


class Arco:
    def __init__(self, origen, destino, etiqueta):
        self.origen = origen
        self.destino = destino
        self.etiqueta = etiqueta

    def __str__(self):
        return f"{self.origen.etiqueta} -- {self.etiqueta} --> {self.destino.etiqueta}"


class RedSemantica:
    def __init__(self):
        self.nodos = []

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
            print(f"- {conclusion}")

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


if __name__ == "__main__":
    # Inicializar la red semántica
    red = RedSemantica()

    # Crear nodos en la red semántica
    fiebre_alta = red.crear_nodo("Fiebre Alta")
    dolor_muscular = red.crear_nodo("Dolor Muscular")
    dificultad_respirar = red.crear_nodo("Dificultad para Respirar")
    gripe = red.crear_nodo("Gripe")
    neumonia = red.crear_nodo("Neumonía")

    # Crear relaciones (arcos) entre nodos
    fiebre_alta.agregar_arco(gripe, "es síntoma de")
    dolor_muscular.agregar_arco(gripe, "es síntoma de")
    fiebre_alta.agregar_arco(neumonia, "es síntoma de")
    dificultad_respirar.agregar_arco(neumonia, "es síntoma de")

    # Mostrar la red semántica
    red.mostrar_red()

    # Inicializar el sistema experto con hechos ingresados por el usuario
    sistema_experto = SistemaExperto(red)

    # Obtener hechos del usuario y procesar la red semántica
    sistema_experto.obtener_hechos_y_evaluar()
