import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Vehicle Market Dashboard", layout="wide")

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")
    return df

df = load_data()

# =========================
# TÍTULO
# =========================
st.title("🚗 Vehicle Market Analysis Dashboard")
st.markdown("Exploratory analysis of vehicle listings in the U.S.")

# =========================
# SIDEBAR (FILTROS)
# =========================
st.sidebar.header("🔎 Filters")

# Filtro de precio
price_min, price_max = st.sidebar.slider(
    "Price Range",
    int(df["price"].min()),
    int(df["price"].max()),
    (int(df["price"].min()), int(df["price"].max()))
)

# Filtro de año
year_min, year_max = st.sidebar.slider(
    "Model Year",
    int(df["model_year"].min()),
    int(df["model_year"].max()),
    (int(df["model_year"].min()), int(df["model_year"].max()))
)

# Filtro por tipo de vehículo
vehicle_types = st.sidebar.multiselect(
    "Vehicle Type",
    options=df["type"].dropna().unique(),
    default=df["type"].dropna().unique()
)

# =========================
# APLICAR FILTROS
# =========================
filtered_df = df[
    (df["price"] >= price_min) &
    (df["price"] <= price_max) &
    (df["model_year"] >= year_min) &
    (df["model_year"] <= year_max) &
    (df["type"].isin(vehicle_types))
]

# =========================
# KPIs
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Vehicles", len(filtered_df))
col2.metric("Average Price", f"${int(filtered_df['price'].mean()):,}")
col3.metric("Average Mileage", f"{int(filtered_df['odometer'].mean()):,}")

st.markdown("---")

# =========================
# GRÁFICOS
# =========================

col1, col2 = st.columns(2)

# Histograma
with col1:
    fig_hist = px.histogram(
        filtered_df,
        x="odometer",
        title="Mileage Distribution",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Scatter
with col2:
    fig_scatter = px.scatter(
        filtered_df,
        x="odometer",
        y="price",
        color="type",
        title="Price vs Mileage",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# TABLA
# =========================
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)
