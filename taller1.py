# =========================================================
# TALLER DE LABORATORIO: MOTOR DE FRAUDE BANCARIO (40 MIN)
# Motor de inferencia por encadenamiento hacia adelante
# (forward chaining) aplicado a deteccion de fraude.
#
# Los HECHOS iniciales ahora se piden por consola (dinamico).
# La base de REGLAS se queda fija: es el "conocimiento experto"
# del sistema, no algo que el usuario deba escribir cada vez.
# =========================================================

import operator

# ---------------------------------------------------------
# 0. Operadores soportados por las reglas
# ---------------------------------------------------------
# El motor del ejemplo original solo comparaba con "==".
# Para poder escribir reglas como [monto > 5000] necesitamos
# mas operadores. Cada condicion ahora es una tupla:
#   (variable, operador, valor)
OPERADORES = {
    "==": operator.eq,
    "!=": operator.ne,
    ">":  operator.gt,
    "<":  operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

# ---------------------------------------------------------
# 1. Base de Reglas (conocimiento experto, no se pide por consola)
# ---------------------------------------------------------
# Cada regla tiene:
#   id          -> nombre de la regla
#   condiciones -> lista de tuplas (variable, operador, valor)
#                  TODAS deben cumplirse (compuerta AND via all())
#   conclusion  -> hechos nuevos que se agregan si la regla dispara
reglas = [
    {
        "id": "R1",
        "condiciones": [("monto", ">", 5000)],
        "conclusion": {"transaccion_inusual": True},
    },
    {
        "id": "R2",
        "condiciones": [
            ("transaccion_inusual", "==", True),
            ("pais_extranjero", "==", True),
        ],
        "conclusion": {"bloquear_tarjeta": True},
    },
    {
        "id": "R3",
        "condiciones": [("intentos_fallidos", ">=", 3)],
        "conclusion": {"actividad_sospechosa": True},
    },
    {
        "id": "R4",
        "condiciones": [
            ("actividad_sospechosa", "==", True),
            ("ip_sospechosa", "==", True),
        ],
        "conclusion": {"bloquear_tarjeta": True},
    },
    {
        "id": "R5",
        "condiciones": [("bloquear_tarjeta", "==", True)],
        "conclusion": {"notificar_seguridad": True},
    },
]


# ---------------------------------------------------------
# 2. Entrada de datos dinamica (hechos iniciales)
# ---------------------------------------------------------
def pedir_entero(mensaje, por_defecto):
    """Pide un numero entero por consola; si el usuario no escribe
    nada, usa el valor por defecto. Repite si el texto no es valido."""
    while True:
        texto = input(f"{mensaje} [{por_defecto}]: ").strip()
        if texto == "":
            return por_defecto
        try:
            return int(texto)
        except ValueError:
            print("  -> Escribe un numero entero valido. Intenta de nuevo.")


def pedir_booleano(mensaje, por_defecto):
    """Pide s/n por consola y lo convierte a True/False."""
    default_txt = "s" if por_defecto else "n"
    while True:
        texto = input(f"{mensaje} (s/n) [{default_txt}]: ").strip().lower()
        if texto == "":
            return por_defecto
        if texto in ("s", "si", "true", "1"):
            return True
        if texto in ("n", "no", "false", "0"):
            return False
        print("  -> Responde con 's' (si) o 'n' (no). Intenta de nuevo.")


def pedir_hechos_iniciales():
    """Construye el diccionario de hechos preguntando al usuario
    los datos de la transaccion a evaluar."""
    print("=== Ingresa los datos de la transaccion a evaluar ===")
    print("(Enter en vacio usa el valor por defecto entre corchetes)\n")

    hechos = {
        "monto": pedir_entero("Monto de la transaccion", 6000),
        "pais_extranjero": pedir_booleano("Pais extranjero?", True),
        "ip_sospechosa": pedir_booleano("IP marcada como sospechosa?", False),
        "intentos_fallidos": pedir_entero("Intentos fallidos de login", 4),
    }
    print()
    return hechos


# ---------------------------------------------------------
# 3. Motor de Inferencia Forward Chaining
# ---------------------------------------------------------
def evaluar_condicion(hechos, condicion):
    """Evalua una condicion (variable, operador, valor) contra los hechos."""
    variable, op, valor = condicion
    if variable not in hechos:
        return False
    return OPERADORES[op](hechos[variable], valor)


def motor_inferencia(hechos, reglas):
    """Ejecuta el ciclo de encadenamiento hacia adelante hasta que
    ninguna regla nueva pueda disparar. Modifica 'hechos' en sitio."""
    nuevos_hechos = True
    while nuevos_hechos:
        nuevos_hechos = False
        for regla in reglas:
            # all() actua como compuerta logica AND: solo es True si
            # CADA condicion de la regla se cumple sobre los hechos actuales.
            condiciones_cumplidas = all(
                evaluar_condicion(hechos, condicion)
                for condicion in regla["condiciones"]
            )

            if condiciones_cumplidas:
                for clave, valor in regla["conclusion"].items():
                    if clave not in hechos:  # Si es un HECHO NUEVO
                        hechos[clave] = valor
                        nuevos_hechos = True  # Dispara un nuevo ciclo
                        print(f"Disparando {regla['id']} -> Nuevo hecho: {clave}={valor}")
    return hechos


# ---------------------------------------------------------
# 4. Programa principal
# ---------------------------------------------------------
if __name__ == "__main__":
    hechos = pedir_hechos_iniciales()

    print("=== Ejecutando motor de inferencia ===")
    motor_inferencia(hechos, reglas)

    print("\nMemoria final:", hechos)

    if hechos.get("bloquear_tarjeta"):
        print("\nRESULTADO: Tarjeta BLOQUEADA por encadenamiento de reglas.")
    else:
        print("\nRESULTADO: Transaccion sin bloqueo.")
