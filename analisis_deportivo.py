
# analisis_deportivo.py
# Proyecto: Estadísticas de Resultados Deportivos – Torneo Apertura 2024
# Escenario D – Organización Empresarial (UTN TUP)
# Autor: Cabro (simulando roles Hugo / Paco / Luis)
# Trazabilidad Jira: PROY-2 – Desarrollo del script de análisis estadístico


# Importamos las librerías necesarias.
# pandas nos permite trabajar con datos tabulares de forma sencilla y eficiente.
# matplotlib es la librería estándar para generar gráficos en Python.
# os nos ayuda a construir rutas relativas compatibles con cualquier sistema.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


# CONFIGURACIÓN DE RUTAS RELATIVAS
# Usamos rutas relativas al directorio del script para garantizar
# que el código se ejecute correctamente en Google Colab sin modificaciones.


# Detectamos la carpeta raíz del proyecto (un nivel arriba de /scripts)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUTA_DATOS      = os.path.join(BASE_DIR, "datos", "resultados_torneo.csv")
RUTA_RESULTADOS = os.path.join(BASE_DIR, "resultados")

# Creamos la carpeta /resultados si todavía no existe
os.makedirs(RUTA_RESULTADOS, exist_ok=True)


# 1. CARGA DE DATOS
# Leemos el dataset en un DataFrame de pandas.
# El archivo contiene una fila por partido con: fecha, equipos y goles.

print("=" * 60)
print("  ANÁLISIS ESTADÍSTICO – TORNEO APERTURA 2024")
print("=" * 60)

df = pd.read_csv(RUTA_DATOS, parse_dates=["fecha"])

print(f"\nDataset cargado correctamente: {len(df)} partidos registrados.\n")
print(df.head())


# 2. CÁLCULO DE ESTADÍSTICAS POR EQUIPO
# Para cada partido hay dos equipos involucrados (local y visitante).
# Procesamos ambas perspectivas y las combinamos en una tabla única.


equipos = sorted(
    set(df["equipo_local"].unique()) | set(df["equipo_visitante"].unique())
)

# Función auxiliar que calcula las estadísticas de un equipo dado
def calcular_stats(nombre_equipo):
    """
    Recorre todos los partidos en los que participó el equipo
    (ya sea como local o visitante) y acumula victorias, empates,
    derrotas y goles a favor / en contra.
    """
    partidos_como_local    = df[df["equipo_local"]     == nombre_equipo]
    partidos_como_visitante = df[df["equipo_visitante"] == nombre_equipo]

    # --- Partidos como LOCAL ---
    v_local = (partidos_como_local["goles_local"] > partidos_como_local["goles_visitante"]).sum()
    e_local = (partidos_como_local["goles_local"] == partidos_como_local["goles_visitante"]).sum()
    d_local = (partidos_como_local["goles_local"] < partidos_como_local["goles_visitante"]).sum()
    gf_local = partidos_como_local["goles_local"].sum()
    gc_local = partidos_como_local["goles_visitante"].sum()

    # --- Partidos como VISITANTE ---
    v_vis = (partidos_como_visitante["goles_visitante"] > partidos_como_visitante["goles_local"]).sum()
    e_vis = (partidos_como_visitante["goles_visitante"] == partidos_como_visitante["goles_local"]).sum()
    d_vis = (partidos_como_visitante["goles_visitante"] < partidos_como_visitante["goles_local"]).sum()
    gf_vis = partidos_como_visitante["goles_visitante"].sum()
    gc_vis = partidos_como_visitante["goles_local"].sum()

    # --- Totales ---
    PJ = v_local + e_local + d_local + v_vis + e_vis + d_vis
    PG = v_local + v_vis
    PE = e_local + e_vis
    PP = d_local + d_vis
    GF = int(gf_local + gf_vis)
    GC = int(gc_local + gc_vis)
    DIF = GF - GC
    # Sistema de puntos estándar: 3 por victoria, 1 por empate
    PTS = PG * 3 + PE * 1

    return {
        "Equipo": nombre_equipo,
        "PJ": int(PJ),
        "PG": int(PG),
        "PE": int(PE),
        "PP": int(PP),
        "GF": GF,
        "GC": GC,
        "DIF": DIF,
        "PTS": int(PTS),
    }

# Construimos el DataFrame de la tabla de posiciones
stats_lista = [calcular_stats(eq) for eq in equipos]
tabla = pd.DataFrame(stats_lista)

# Ordenamos: primero por puntos, luego por diferencia de goles como desempate
tabla = tabla.sort_values(["PTS", "DIF", "GF"], ascending=False).reset_index(drop=True)
tabla.index += 1  # Posición empieza en 1

print("\n" + "=" * 60)
print("  TABLA DE POSICIONES")
print("=" * 60)
print(tabla.to_string())



# 3. ESTADÍSTICAS GLOBALES DEL TORNEO
# Calculamos métricas generales que dan contexto al análisis.


total_partidos = len(df)
total_goles    = int(df["goles_local"].sum() + df["goles_visitante"].sum())
promedio_goles = round(total_goles / total_partidos, 2)

# Equipo con más victorias (mayor PG)
mejor_equipo = tabla.iloc[0]["Equipo"]
max_victorias = tabla.iloc[0]["PG"]

# Partido con más goles en total
df["total_goles"] = df["goles_local"] + df["goles_visitante"]
idx_max = df["total_goles"].idxmax()
partido_mas_goles = df.loc[idx_max]

print("\n" + "=" * 60)
print("  ESTADÍSTICAS GLOBALES DEL TORNEO")
print("=" * 60)
print(f"  Total de partidos jugados : {total_partidos}")
print(f"  Total de goles marcados   : {total_goles}")
print(f"  Promedio de goles/partido : {promedio_goles}")
print(f"  Equipo líder              : {mejor_equipo} ({max_victorias} victorias)")
print(f"  Partido con más goles     : {partido_mas_goles['equipo_local']} "
      f"{int(partido_mas_goles['goles_local'])}-{int(partido_mas_goles['goles_visitante'])} "
      f"{partido_mas_goles['equipo_visitante']} "
      f"({partido_mas_goles['total_goles']} goles)")



# 4. EXPORTACIÓN DE RESULTADOS A CSV
# Guardamos la tabla de posiciones como archivo CSV en /resultados
# para que quede disponible como evidencia reproducible del análisis.

ruta_tabla = os.path.join(RUTA_RESULTADOS, "tabla_posiciones.csv")
tabla.to_csv(ruta_tabla)
print(f"\n  Tabla exportada en: {ruta_tabla}")



# 5. GENERACIÓN DE GRÁFICOS
# Producimos dos visualizaciones complementarias:
#   a) Gráfico de barras comparativo de PTS, PG, PE, PP por equipo
#   b) Gráfico de barras de goles a favor vs goles en contra


colores_base = ["#2ecc71", "#e67e22", "#e74c3c", "#3498db"]

# ---- Gráfico 1: Rendimiento comparativo por equipo ----
fig1, ax1 = plt.subplots(figsize=(12, 6))

x          = range(len(tabla))
ancho_barra = 0.2

ax1.bar([i - ancho_barra*1.5 for i in x], tabla["PTS"], width=ancho_barra,
        label="Puntos",    color="#2980b9")
ax1.bar([i - ancho_barra*0.5 for i in x], tabla["PG"],  width=ancho_barra,
        label="Victorias", color="#27ae60")
ax1.bar([i + ancho_barra*0.5 for i in x], tabla["PE"],  width=ancho_barra,
        label="Empates",   color="#f39c12")
ax1.bar([i + ancho_barra*1.5 for i in x], tabla["PP"],  width=ancho_barra,
        label="Derrotas",  color="#c0392b")

ax1.set_xticks(list(x))
ax1.set_xticklabels(tabla["Equipo"], rotation=15, ha="right", fontsize=11)
ax1.set_ylabel("Cantidad", fontsize=12)
ax1.set_title("Rendimiento Comparativo por Equipo – Torneo Apertura 2024",
              fontsize=13, fontweight="bold", pad=14)
ax1.legend(fontsize=10)
ax1.set_ylim(0, tabla["PTS"].max() + 4)
ax1.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
ruta_g1 = os.path.join(RUTA_RESULTADOS, "grafico_rendimiento.png")
fig1.savefig(ruta_g1, dpi=150)
plt.close(fig1)
print(f"  Gráfico 1 guardado en  : {ruta_g1}")


# ---- Gráfico 2: Goles a favor vs Goles en contra ----
fig2, ax2 = plt.subplots(figsize=(12, 5))

x2 = range(len(tabla))
ax2.bar([i - ancho_barra*0.5 for i in x2], tabla["GF"], width=ancho_barra,
        label="Goles a favor",    color="#1abc9c")
ax2.bar([i + ancho_barra*0.5 for i in x2], tabla["GC"], width=ancho_barra,
        label="Goles en contra",  color="#e74c3c", alpha=0.85)

ax2.set_xticks(list(x2))
ax2.set_xticklabels(tabla["Equipo"], rotation=15, ha="right", fontsize=11)
ax2.set_ylabel("Goles", fontsize=12)
ax2.set_title("Goles a Favor vs. Goles en Contra por Equipo",
              fontsize=13, fontweight="bold", pad=14)
ax2.legend(fontsize=10)
ax2.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
ruta_g2 = os.path.join(RUTA_RESULTADOS, "grafico_goles.png")
fig2.savefig(ruta_g2, dpi=150)
plt.close(fig2)
print(f"  Gráfico 2 guardado en  : {ruta_g2}")

print("\n  Análisis completado exitosamente.\n")
