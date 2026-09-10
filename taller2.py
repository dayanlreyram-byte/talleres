# =========================================================
# TALLER DE LABORATORIO: LOGICA DIFUSA COMERCIAL (40 MIN)
# Clasificacion de la "Experiencia" de un conductor mediante
# conjuntos difusos triangulares.
# =========================================================


def membresia_triangular(x, a, b, c):
    """Funcion de membresia triangular a trozos.

    a = vertice izquierdo (grado 0)
    b = vertice superior  (grado 1)
    c = vertice derecho   (grado 0)
    """
    # Implementacion computacional de las funciones a trozos
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)


# ---------------------------------------------------------
# 1. Definicion de los conjuntos difusos para "Experiencia"
#    (anios trabajados -> vertices del triangulo)
# ---------------------------------------------------------
conjuntos_experiencia = {
    "Novato":     (0, 0, 5),
    "Intermedio": (2, 5, 8),
    "Experto":    (5, 10, 20),
}

# ---------------------------------------------------------
# 2. Conductores a evaluar (anios de experiencia)
# ---------------------------------------------------------
conductores = [3, 6, 12]

# ---------------------------------------------------------
# 3. Ciclo de evaluacion: calcula los 3 grados de membresia
#    de cada conductor y determina su categoria dominante
# ---------------------------------------------------------
for anios in conductores:
    print(f"=== Conductor con {anios} anios de experiencia ===")

    # Calculamos el grado de pertenencia a cada conjunto difuso
    grados = {
        categoria: membresia_triangular(anios, *vertices)
        for categoria, vertices in conjuntos_experiencia.items()
    }

    for categoria, grado in grados.items():
        print(f"- Pertenece a {categoria.upper()} en un {grado * 100:.1f}%")

    # 4. Categoria dominante: la de mayor grado de verdad.
    # max() con key=grados.get busca, entre las claves del
    # diccionario, la que tiene el valor (grado) mas alto.
    categoria_dominante = max(grados, key=grados.get)
    print(f"-> Categoria dominante: {categoria_dominante} "
          f"(grado {grados[categoria_dominante] * 100:.1f}%)\n")
