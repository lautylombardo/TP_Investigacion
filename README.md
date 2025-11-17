# TP Investigación: Análisis de Salarios por Sector CLAE

## Descripción
Análisis de la evolución salarial en Argentina por sector económico (CLAE 3 dígitos) desde 2007 a 2023.

## Estructura del Proyecto

```
.
├── Main.py              # Script principal de análisis
├── Clases.csv           # Diccionario CLAE (clasificación de actividades)
├── Mensuales.csv        # Datos de salarios medianos mensuales por sector
├── README.md            # Este archivo
└── .gitignore           # Configuración de Git
```

## Datos

### `Clases.csv`
Diccionario con la clasificación de actividades económicas (CLAE):
- `clae6`: Clasificación a 6 dígitos (nivel más detallado)
- `clae3`: Clasificación a 3 dígitos (220 sectores)
- `clae2`: Clasificación a 2 dígitos
- `letra`: Macro-sector (A-U)
- Descripciones en cada nivel

**Fuente**: Instituto Nacional de Estadística y Censos (INDEC) - Argentina

### `Mensuales.csv`
Datos mensuales de salarios medianos:
- `fecha`: Fecha (desde 2007-01 hasta 2023-12)
- `clae3`: Sector CLAE 3 dígitos
- `w_median`: Salario mediano (en ARS)

## Features Generadas

El script `Main.py` genera automáticamente:

1. **Columnas temporales**
   - `anio`: Año
   - `mes`: Mes

2. **Variaciones**
   - `var_mensual`: Variación mes a mes (%)
   - `var_anual`: Variación año a año (%)

3. **Rankings**
   - `ranking_anual`: Ranking de sectores por salario dentro de cada año

4. **Análisis comparativo**
   - `desvio_sector`: Desviación respecto al salario promedio del macro-sector

## Uso

```bash
python Main.py
```

Esto generará:
- Estadísticas descriptivas
- Tabla con primeros registros
- Gráfico de evolución salarial promedio
- Información sobre datos faltantes

## Estadísticas Básicas

- **Períodos**: 2007 - 2023 (17 años)
- **Sectores**: 220 categorías CLAE-3
- **Registros**: 44,650 observaciones
- **Salario mediano promedio**: ~47,014 ARS
- **Rango**: -99 a 2,297,984 ARS

## Dependencias

```
pandas>=2.0
matplotlib>=3.10
seaborn>=0.13
scipy>=1.16
numpy>=2.3
```

### Instalación

```bash
pip install pandas matplotlib seaborn scipy numpy
```

## Próximas Mejoras

- [ ] Análisis de concentración salarial (Gini)
- [ ] Identificación de outliers y anomalías
- [ ] Clustering de sectores
- [ ] Dashboards interactivos con Plotly
- [ ] Modelos predictivos para 2024-2025

## Autor

Lauty - TP Investigación

## Fecha

Noviembre 2025
