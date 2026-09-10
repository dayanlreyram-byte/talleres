# =========================================================
# TALLER DE LABORATORIO: MOTOR LOGICO DE RECURSOS HUMANOS (40 MIN)
# Motor de inferencia difusa (Mamdani) que calcula el nivel de
# activacion de un bono segun el Desempeno y la Antiguedad.
# =========================================================

# ---------------------------------------------------------
# 1. Grados de membresia actuales (resultado de la fuzzificacion)
# ---------------------------------------------------------
# Variables difusas de entrada, ya "fuzzificadas" (valor entre 0 y 1
# que indica que tanto pertenece el empleado a cada categoria).
grados = {
    "desempeno_pobre": 0.1,
    "desempeno_promedio": 0.3,
    "desempeno_excelente": 0.85,
    "antiguedad_corta": 0.2,
    "antiguedad_larga": 0.6,
}


# ---------------------------------------------------------
# 2. Evaluacion de reglas Mamdani
#    AND -> min()   OR -> max()
# ---------------------------------------------------------
def evaluar_reglas_rrhh(grados):
    # REGLA 1: SI Desempeno es POBRE O Antiguedad es CORTA
    #          ENTONCES Bono = BAJO
    fuerza_or = max(grados["desempeno_pobre"], grados["antiguedad_corta"])
    activacion_bono_bajo = fuerza_or

    # REGLA 2: SI Desempeno es PROMEDIO
    #          ENTONCES Bono = MEDIO
    # (una sola condicion: el grado de activacion es el mismo grado
    #  de membresia de "desempeno_promedio")
    activacion_bono_medio = grados["desempeno_promedio"]

    # REGLA 3: SI Desempeno es EXCELENTE Y Antiguedad es LARGA
    #          ENTONCES Bono = ALTO
    activacion_bono_alto = min(grados["desempeno_excelente"], grados["antiguedad_larga"])

    return {
        "BONO_BAJO": activacion_bono_bajo,
        "BONO_MEDIO": activacion_bono_medio,
        "BONO_ALTO": activacion_bono_alto,
    }


# ---------------------------------------------------------
# 3. Ejecucion: el motor retorna un diccionario con los
#    niveles de activacion para Bono Bajo, Medio y Alto.
# ---------------------------------------------------------
fuerza_conclusiones = evaluar_reglas_rrhh(grados)
print("Fuerza de activacion para cada conclusion:", fuerza_conclusiones)

for bono, fuerza in fuerza_conclusiones.items():
    print(f"- {bono}: {fuerza * 100:.1f}%")

bono_dominante = max(fuerza_conclusiones, key=fuerza_conclusiones.get)
print(f"\nRESULTADO: La conclusion dominante es {bono_dominante} "
      f"con fuerza {fuerza_conclusiones[bono_dominante] * 100:.1f}%")


# ---------------------------------------------------------
# 4. Pregunta teorica
# ---------------------------------------------------------
# Si dos reglas DIFERENTES concluyen en la misma etiqueta difusa
# ("Bono Alto"), con fuerzas de activacion 0.4 y 0.7, el paso de
# AGREGACION de Mamdani debe combinar ambas salidas parciales en
# una sola superficie de salida para "Bono Alto". Como basta con
# que UNA de las dos reglas se cumpla fuertemente para que la
# conclusion quede "encendida", se usa la T-Conorma, es decir el
# operador logico OR -> max().
#
# La linea de codigo para esto es:
fuerza_final_bono_alto = max(0.4, 0.7)
print(f"\nPregunta teorica -> Fuerza final agregada de 'Bono Alto': "
      f"{fuerza_final_bono_alto}")
