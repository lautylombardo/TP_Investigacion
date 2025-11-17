import pandas as pd
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

# Columna auxiliar de año
merged_df["anio"] = merged_df["fecha"].dt.year

# -------------------------------------------------------------------
# GRÁFICO 1: Serie temporal global con slider de tiempo
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

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# -------------------------------------------------------------------
# GRÁFICO 2: Barras + tabla de descripciones al costado
# -------------------------------------------------------------------

# Promedio salarial por letra
salario_por_letra = (
    merged_df.groupby("letra", as_index=False)["w_median"]
    .mean()
    .sort_values("w_median", ascending=False)
)

# Descripciones únicas por letra (ordenadas por letra)
letras_desc = (
    merged_df[["letra", "letra_desc"]]
    .drop_duplicates()
    .sort_values("letra")
)

# Creamos figura con 2 columnas: bar (col 1) + table (col 2)
fig2 = make_subplots(
    rows=1, cols=2,
    column_widths=[0.55, 0.45],
    specs=[[{"type": "bar"}, {"type": "table"}]],
    horizontal_spacing=0.08,
    subplot_titles=("Salario mediano por letra (CLAE)", "Descripción por letra")
)

# --- Columna 1: Barras ---
fig2.add_trace(
    go.Bar(
        x=salario_por_letra["letra"],
        y=salario_por_letra["w_median"],
        marker_color="royalblue",
        customdata=salario_por_letra["letra"].map(
            dict(zip(letras_desc["letra"], letras_desc["letra_desc"]))
        ),
        hovertemplate="<b>Letra: %{x}</b><br>Descripción: %{customdata}<br>Salario: %{y:$,.2f}<extra></extra>"
    ),
    row=1, col=1
)

fig2.update_xaxes(title_text="Letra (CLAE)", row=1, col=1)
fig2.update_yaxes(title_text="Salario mediano promedio (ARS)", row=1, col=1)

# --- Columna 2: Tabla con letra + descripción ---
fig2.add_trace(
    go.Table(
        header=dict(
            values=["Letra", "Descripción del sector"],
            fill_color="lightgrey",
            align="left",
            font=dict(size=12, color="black")
        ),
        cells=dict(
            values=[letras_desc["letra"], letras_desc["letra_desc"]],
            align="left",
            font=dict(size=11),
            height=22
        )
    ),
    row=1, col=2
)

fig2.update_layout(
    title_text="Salario mediano promedio por gran sector económico (letra CLAE)",
    template="plotly_white",
    width=1600,
    height=800,
    showlegend=False
)

fig2.show()

# -------------------------------------------------------------------
# GRÁFICO 3: Top 10 actividades mejor remuneradas con filtro de año
# -------------------------------------------------------------------
# Lista de años disponibles
anios = sorted(merged_df["anio"].unique())

# Función auxiliar para calcular top10 por año
def top10_por_anio(anio):
    df_anio = (
        merged_df[merged_df["anio"] == anio]
        .groupby(["clae3", "clae3_desc"])["w_median"]
        .mean()
        .reset_index()
        .sort_values("w_median", ascending=False)
        .head(10)
        .sort_values("w_median")  # para ordenar de menor a mayor y que quede prolijo el barh
    )
    return df_anio

# Usamos el primer año como inicial
anio_inicial = anios[0]
df_ini = top10_por_anio(anio_inicial)

fig3 = px.bar(
    df_ini,
    x="w_median",
    y="clae3_desc",
    orientation="h",
    title=f"Top 10 actividades mejor remuneradas - Año {anio_inicial}",
    labels={"w_median": "Salario mediano promedio (ARS)", "clae3_desc": "Actividad económica (CLAE3)"}
)

# Precalculamos datos por año para el dropdown
data_por_anio = {anio: top10_por_anio(anio) for anio in anios}

botones = []
for anio in anios:
    df_anio = data_por_anio[anio]
    botones.append(
        dict(
            label=str(anio),
            method="update",
            args=[
                {
                    "x": [df_anio["w_median"]],
                    "y": [df_anio["clae3_desc"]]
                },
                {
                    "title": f"Top 10 actividades mejor remuneradas - Año {anio}"
                }
            ]
        )
    )

fig3.update_layout(
    updatemenus=[
        dict(
            buttons=botones,
            direction="down",
            x=1.15,
            xanchor="left",
            y=1,
            yanchor="top",
            showactive=True,
        )
    ]
)

fig3.show()
# -------------------------------------------------------------------
# GRÁFICO 4: Gráfico de torta por sector (último año disponible)
# -------------------------------------------------------------------
# Aseguramos tener la columna 'anio'
merged_df["anio"] = merged_df["fecha"].dt.year

ultimo_anio = merged_df["anio"].max()

df_pie = (
    merged_df[merged_df["anio"] == ultimo_anio]
    .groupby(["letra", "letra_desc"], as_index=False)["w_median"]
    .mean()
)

fig4 = px.pie(
    df_pie,
    names="letra_desc",          # en la torta se ve el nombre del sector
    values="w_median",           # usamos el salario mediano promedio
    title=f"Participación relativa del salario mediano promedio por sector - Año {ultimo_anio}",
    hover_data={"letra": True, "w_median": ':.2f'}
)

# Mostramos porcentaje + etiqueta dentro de cada porción
fig4.update_traces(textposition="inside", textinfo="percent+label")
fig4.show()
