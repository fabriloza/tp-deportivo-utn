# Estadísticas de Resultados Deportivos – Torneo Apertura 2024

Cátedra:Organización Empresarial  
Institución:UTN – Tecnicatura Universitaria en Programación (TUP)  
Año Lectivo: 2026  
Escenario elegido: Escenario D – Estadísticas de Resultados Deportivos

---

## Integrante

| Rol 
|-----|----------------|-----------------|
| P1 –Líder y Organizador Fabrizio Loza 

---

## Descripción del proyecto

Este repositorio contiene el análisis estadístico de los resultados de un torneo de fútbol amateur simulado (Torneo Apertura 2024). El script procesa un dataset CSV con los resultados de todos los partidos de la fase de grupos y produce:

- Tabla de posiciones completa (PJ, PG, PE, PP, GF, GC, DIF, PTS)
- Estadísticas globales del torneo (goles totales, promedio por partido, equipo líder)
- Dos gráficos comparativos exportados como imágenes PNG

---

## Dataset utilizado

**Archivo:** `datos/resultados_torneo.csv`  
**Formato:** CSV  
**Fuente:** Dataset simulado generado para fines educativos  
**Columnas:**

| Campo | Descripción |
|-------|-------------|
| `fecha` | Fecha del partido (YYYY-MM-DD) |
| `equipo_local` | Nombre del equipo local |
| `equipo_visitante` | Nombre del equipo visitante |
| `goles_local` | Goles marcados por el equipo local |
| `goles_visitante` | Goles marcados por el equipo visitante |

---

## Estructura del repositorio

```
repo-proyecto/
│
├── datos/
│   └── resultados_torneo.csv       # Dataset de partidos
│
├── scripts/
│   └── analisis_deportivo.py       # Script principal de análisis
│
├── resultados/
│   ├── tabla_posiciones.csv        # Tabla de posiciones exportada
│   ├── grafico_rendimiento.png     # Gráfico comparativo de rendimiento
│   └── grafico_goles.png           # Gráfico de goles a favor vs en contra
│
├── README.md
└── .gitignore
```

---

## Instrucciones para ejecutar el script

### Requisitos

- Python 3.8 o superior
- Librerías: `pandas`, `matplotlib`

### Instalación de dependencias

```bash
pip install pandas matplotlib
```

### Ejecución local

Desde la raíz del repositorio:

```bash
python scripts/analisis_deportivo.py
```

### Ejecución en Google Colab

```python
# 1. Clonar el repositorio
!git clone https://github.com/TU_USUARIO/repo-proyecto.git
%cd repo-proyecto

# 2. Instalar dependencias
!pip install pandas matplotlib

# 3. Ejecutar el script
!python scripts/analisis_deportivo.py
```

Los gráficos y la tabla de posiciones se guardarán automáticamente en la carpeta `/resultados`.

---

## Trazabilidad con Jira

Todos los commits de este repositorio siguen el formato de Conventional Commits vinculado al ID de Issue de Jira correspondiente:

```
PROY-1: Inicializar estructura de carpetas y README
PROY-2: Agregar script de análisis estadístico deportivo
PROY-3: Revisar código, mejorar comentarios y cerrar Pull Request
```

---

## Resultados obtenidos

Al ejecutar el script sobre el dataset incluido se obtiene la siguiente tabla de posiciones:

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DIF | PTS |
|-----|--------|----|----|----|----|----|----|-----|-----|
| 1 | Tigres FC | 8 | 6 | 2 | 0 | 14 | 4 | +10 | 20 |
| 2 | Real Oeste | 8 | 6 | 1 | 1 | 14 | 7 | +7 | 19 |
| 3 | Club Río | 8 | 5 | 1 | 2 | 12 | 9 | +3 | 16 |
| 4 | Estudiantes CF | 8 | 3 | 2 | 3 | 12 | 10 | +2 | 11 |
| 5 | Halcones United | 8 | 2 | 2 | 4 | 11 | 10 | +1 | 8 |
| 6 | Los Pumas | 8 | 2 | 1 | 5 | 8 | 14 | -6 | 7 |
| 7 | Atlético Norte | 8 | 1 | 2 | 5 | 7 | 14 | -7 | 5 |
| 8 | Deportivo Sur | 8 | 1 | 1 | 6 | 5 | 15 | -10 | 4 |

**Promedio de goles por partido:** 2.59  
**Total de goles en el torneo:** 83
