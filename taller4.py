# =========================================================
# TALLER DE LABORATORIO: DEFUZZIFICACION (40 MIN)
# Implementacion propia del metodo del Centroide (COG) usando
# operaciones matriciales de NumPy (no requiere skfuzzy).
# =========================================================

import numpy as np


def centroide(x, curva):
    """Calcula el Centro de Gravedad (COG) de una curva difusa.

    x     -> array con los valores del universo del discurso (eje X)
    curva -> array con el grado de membresia (altura) en cada punto

    Formula:  COG = sum(x * curva) / sum(curva)
    """
    x = np.asarray(x, dtype=float)
    curva = np.asarray(curva, dtype=float)
    return np.sum(x * curva) / np.sum(curva)


# ---------------------------------------------------------
# 1 y 2. Validacion con los datos del Taller Analitico
# ---------------------------------------------------------
x_validacion = [10, 20, 30, 40]
mu_validacion = [0.2, 0.8, 0.8, 0]

resultado_validacion = centroide(x_validacion, mu_validacion)
print("=== Validacion de la funcion centroide() ===")
print(f"x  = {x_validacion}")
print(f"mu = {mu_validacion}")
print(f"COG calculado = {resultado_validacion:.4f}")
print("(debe coincidir con el resultado obtenido a mano en el taller analitico)\n")


# ---------------------------------------------------------
# 3. Nuevo escenario: sistema de frenado automatico
#    Eje X = fuerza de frenado, de 0 a 100 Newtons.
# ---------------------------------------------------------
x_frenado = np.linspace(0, 100, 100)

# Curva de campana de Gauss centrada en 70, usando np.exp().
# sigma controla el "ancho" de la campana; se elige 10 como un
# valor razonable para que la curva quede bien contenida dentro
# del universo del discurso (0 a 100).
centro = 70
sigma = 10
curva_frenado = np.exp(-0.5 * ((x_frenado - centro) / sigma) ** 2)

# ---------------------------------------------------------
# 4. Defuzzificacion: se aplica la misma funcion centroide()
#    para obtener el valor CRISP (exacto) de fuerza de frenado.
# ---------------------------------------------------------
fuerza_frenado_crisp = centroide(x_frenado, curva_frenado)

print("=== Escenario: sistema de frenado automatico ===")
print(f"Universo del discurso: {len(x_frenado)} puntos entre 0 y 100 N")
print(f"Campana de Gauss centrada en {centro} N (sigma={sigma})")
print(f"Fuerza de frenado exacta (defuzzificada): {fuerza_frenado_crisp:.2f} N")
