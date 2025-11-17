import pandas as pd
import matplotlib.pyplot as plt  # lo podés dejar por si usás algo estático
import plotly.express as px

# -------------------------------
# 1) Cargar los archivos CSV
# -------------------------------

clases_df = pd.read_csv("Clases.csv", sep=",")
mensuales_df = pd.read_csv("Mensuales.csv", sep=",")

# -------------------------------
# 2) Mostrar información básica
# -------------------------------

print("===== ARCHIVO CLASES (Diccionario CLAE) =====")
print("Filas y columnas:", clases_df.shape)
print(clases_df.head(), "\n")   # primeras 5 filas

print("===== ARCHIVO MENSUALES (Salarios) =====")
print("Filas y columnas:", mensuales_df.shape)
print(mensuales_df.head())

# === Convertir la columna fecha a tipo datetime ===
mensuales_df["fecha"] = pd.to_datetime(mensuales_df["fecha"])

# === Seleccionar solo columnas útiles del diccionario CLAE ===
clases_simple = clases_df[["clae3", "clae3_desc", "clae2", "clae2_desc",
                           "letra", "letra_desc"]].drop_duplicates()

# === Hacer el merge (join) ===
merged_df = mensuales_df.merge(clases_simple, on="clae3", how="left")

# === Validar resultado ===
print("===== MERGED (Mensuales + Diccionario CLAE) =====")
print("Filas y columnas:", merged_df.shape)
print(merged_df.head())

print("===== INFO GENERAL =====")
print(merged_df.info(), "\n")

print("===== SALARIO (ESTADÍSTICAS) =====")
print(merged_df["w_median"].describe(), "\n")

print("===== AÑOS DISPONIBLES =====")
print(sorted(merged_df["fecha"].dt.year.unique()), "\n")

print("===== SECTORES (CLAE 3 DÍGITOS) =====")
print("Cantidad:", merged_df["clae3"].nunique())
print(merged_df["clae3"].unique()[:20], "...", "\n")

print("===== VALORES FALTANTES =====")
print(merged_df.isna().sum())

# -------------------------------------------------------------------
# GRAFICO 1 (INTERACTIVO):
# Evolución del salario mediano promedio (2007–2022)
# -------------------------------------------------------------------
promedios_tiempo = (
    merged_df.groupby("fecha")["w_median"]
    .mean()
    .reset_index()
)

fig1 = px.line(
    promedios_tiempo,
    x="fecha",
    y="w_median",
    title="Evolución del salario mediano promedio (2007–2022)",
    labels={"fecha": "Fecha", "w_median": "Salario mediano (ARS)"}
)
fig1.update_layout(xaxis_rangeslider_visible=True)
fig1.show()

# -------------------------------------------------------------------
# GRAFICO 2 (INTERACTIVO):
# Salario promedio por letra (gran sector económico)
# -------------------------------------------------------------------
salario_por_letra = (
    merged_df.groupby("letra")["w_median"]
    .mean()
    .reset_index()
    .sort_values("w_median", ascending=False)
)

fig2 = px.bar(
    salario_por_letra,
    x="letra",
    y="w_median",
    title="Salario mediano promedio por gran sector económico (letra CLAE)",
    labels={"letra": "Letra (CLAE)", "w_median": "Salario mediano promedio (ARS)"}
)
fig2.show()

# -------------------------------------------------------------------
# GRAFICO 3 (INTERACTIVO):
# Top 10 sectores (CLAE3) mejor pagos en el último año disponible
# -------------------------------------------------------------------
ultimo_anio = merged_df["fecha"].dt.year.max()
df_ultimo_anio = merged_df[merged_df["fecha"].dt.year == ultimo_anio]

top10_clae3 = (
    df_ultimo_anio
    .groupby(["clae3", "clae3_desc"])["w_median"]
    .mean()
    .reset_index()
    .sort_values("w_median", ascending=False)
    .head(10)
)

fig3 = px.bar(
    top10_clae3.sort_values("w_median"),  # ordeno para que la barra horizontal quede prolija
    x="w_median",
    y="clae3_desc",
    orientation="h",
    title=f"Top 10 actividades mejor remuneradas - Año {ultimo_anio}",
    labels={"w_median": "Salario mediano promedio (ARS)", "clae3_desc": "Actividad económica (CLAE3)"}
)
fig3.show()

# -------------------------------------------------------------------
# GRAFICO 4 (INTERACTIVO):
# Boxplot de salarios por gran sector (letra CLAE)
# -------------------------------------------------------------------
fig4 = px.box(
    merged_df,
    x="letra",
    y="w_median",
    title="Distribución del salario mediano por gran sector económico (letra CLAE)",
    labels={"letra": "Letra (CLAE)", "w_median": "Salario mediano (ARS)"}
)
fig4.show()
