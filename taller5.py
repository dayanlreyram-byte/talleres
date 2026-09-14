# =========================================================
# TALLER ANALITICO: EL ALGORITMO EN PAPEL (20 MIN)
# + Verificacion computacional con Scikit-Learn
# =========================================================
#
# ---------------------------------------------------------
# PARTE 1: Analisis en papel (entropia y ganancia de informacion)
# ---------------------------------------------------------
#
# Conjunto inicial: 6 clientes -> 3 compraron seguro, 3 no.
# La proporcion es 50% / 50%, asi que la entropia inicial es MAXIMA:
#
#   H(S) = -(3/6)*log2(3/6) - (3/6)*log2(3/6)
#        = -0.5*log2(0.5) - 0.5*log2(0.5)
#        = 0.5 + 0.5 = 1 bit
#
# --- Pregunta A: ¿Es mayor de 30 anios? ---
#   Grupo izquierdo (4 personas): [2 compraron, 2 no]  -> 50/50 -> H = 1 bit
#   Grupo derecho   (2 personas): [1 compro,  1 no]    -> 50/50 -> H = 1 bit
#
#   Entropia ponderada tras el split A:
#     H_A = (4/6)*1 + (2/6)*1 = 1 bit
#
#   Ganancia de Informacion (A) = H(S) - H_A = 1 - 1 = 0 bits
#
#   -> La Pregunta A NO reduce el desorden en absoluto: cada subgrupo
#      sigue estando mezclado 50/50, tan "confuso" como el original.
#
# --- Pregunta B: ¿Tiene Auto? ---
#   Grupo izquierdo (3 personas): [3 compraron, 0 no] -> puro -> H = 0 bits
#   Grupo derecho   (3 personas): [0 compraron, 3 no] -> puro -> H = 0 bits
#
#   Entropia ponderada tras el split B:
#     H_B = (3/6)*0 + (3/6)*0 = 0 bits
#
#   Ganancia de Informacion (B) = H(S) - H_B = 1 - 0 = 1 bit
#
#   -> La Pregunta B logra una separacion PERFECTA: cada hoja queda
#      100% pura (o todos compran, o nadie compra).
#
# CONCLUSION 1: La Pregunta B ("¿Tiene Auto?") da la mayor Ganancia
# de Informacion (1 bit contra 0 bits de la Pregunta A), por lo que
# el arbol de decision la elegira como nodo raiz.
#
# CONCLUSION 2 (Regla logica aprendida si B es la raiz y ambas hojas
# quedan puras, es decir, el arbol no necesita mas niveles):
#
#   REGLA 1: SI Tiene_Auto = Si     ENTONCES Compra_Seguro = Si
#   REGLA 2: SI Tiene_Auto = No     ENTONCES Compra_Seguro = No
#
# =========================================================


# ---------------------------------------------------------
# PARTE 2: Verificacion con Scikit-Learn (DecisionTreeClassifier)
# ---------------------------------------------------------
# Reconstruimos los 6 clientes de forma consistente con ambos splits
# (misma poblacion, dos preguntas/features distintas) y dejamos que
# el arbol elija su propio nodo raiz para comprobar la conclusion 1.

from sklearn.tree import DecisionTreeClassifier, export_text

# Features: [mayor_30, tiene_auto]  (1 = Si, 0 = No)
# Target:   compra_seguro           (1 = Si, 0 = No)
X = [
    [0, 1],  # C1: <=30, con auto      -> compro
    [1, 1],  # C2: >30,  con auto      -> compro
    [1, 1],  # C3: >30,  con auto      -> compro
    [0, 0],  # C4: <=30, sin auto      -> no compro
    [1, 0],  # C5: >30,  sin auto      -> no compro
    [1, 0],  # C6: >30,  sin auto      -> no compro
]
y = [1, 1, 1, 0, 0, 0]
nombres_features = ["mayor_30", "tiene_auto"]

# criterion="entropy" para que use exactamente la misma metrica
# (Ganancia de Informacion) calculada a mano arriba.
arbol = DecisionTreeClassifier(criterion="entropy", random_state=0)
arbol.fit(X, y)

print("=== Regla aprendida automaticamente por el arbol de decision ===")
print(export_text(arbol, feature_names=nombres_features))

nodo_raiz = nombres_features[arbol.tree_.feature[0]]
print(f"Nodo raiz elegido por el algoritmo: '{nodo_raiz}'")
print("(confirma que 'tiene_auto' es la pregunta con mayor Ganancia de "
      "Informacion, tal como se calculo a mano en la Parte 1)")
