import pandas as pd

# -------------------------------
# 1) Cargar los archivos CSV
# -------------------------------

# Si están en la misma carpeta que el Main.py:
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
clases_simple = clases_df[["clae3", "clae3_desc", "clae2", "clae2_desc", "letra", "letra_desc"]].drop_duplicates()

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

# -------------------------------
# 3) MEJORAS 1 - Nuevas features
# -------------------------------

# ✔ 1. Crear columnas de año y mes
merged_df["anio"] = merged_df["fecha"].dt.year
merged_df["mes"] = merged_df["fecha"].dt.month

# ✔ 2. Variación mensual
merged_df["var_mensual"] = merged_df.groupby("clae3")["w_median"].pct_change()

# ✔ 3. Variación anual (year-over-year)
merged_df["var_anual"] = merged_df.groupby("clae3")["w_median"].pct_change(12)

# ✔ 4. Ranking por año (descendente)
merged_df["ranking_anual"] = merged_df.groupby("anio")["w_median"].rank(ascending=False)

# ✔ 5. Desviación respecto al salario promedio del sector macro (letra)
sector_mean = merged_df.groupby(["fecha", "letra"])["w_median"].transform("mean")
merged_df["desvio_sector"] = merged_df["w_median"] - sector_mean

print("\n===== NUEVAS FEATURES CREADAS =====")
print(merged_df[["fecha", "clae3", "w_median", "anio", "mes", "var_mensual", "var_anual", "ranking_anual", "desvio_sector"]].head(10))

import matplotlib.pyplot as plt

promedios = merged_df.groupby("fecha")["w_median"].mean()

plt.figure(figsize=(12,6))
plt.plot(promedios.index, promedios.values)
plt.title("Evolución del salario mediano promedio (2007–2022)")
plt.xlabel("Año")
plt.ylabel("Salario mediano (ARS)")
plt.grid(True)
plt.show()
