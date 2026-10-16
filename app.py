import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.forecaster import HYGR_CHANNELS, forecast_hygr_retail_demand, load_macro_consumption_indicators

st.set_page_config(page_title="HYGR 4-Channel Retail Demand Forecaster", layout="wide")
st.title("RETAIL DEMAND FORECASTER (HYGR 4-CHANNEL MATRIX)")
st.caption("Linking National Private Consumption Indicators (Table 3.5) to Retail Channels")

c1, c2, c3 = st.columns(3)
with c1:
    priv_cons = st.slider("2027 Private Consumption Growth (%)", 2.0, 8.0, 4.8, 0.1)
with c2:
    cpi_val = st.slider("2027 CPI Inflation (%)", 1.0, 5.0, 2.3, 0.1)
with c3:
    emp_val = st.slider("2027 Employment Growth (%)", 0.5, 4.0, 2.0, 0.1)

metrics = forecast_hygr_retail_demand(priv_cons, cpi_val, emp_val)
df_m = pd.DataFrame([m.model_dump() for m in metrics])

cols = st.columns(4)
for idx, ch in enumerate(HYGR_CHANNELS):
    sub = df_m[df_m["platform_region"] == ch]
    last_row = sub.iloc[-1]
    with cols[idx]:
        st.metric(f"{ch} (2027-Q2 Fcst)", f"{last_row['macro_predicted_index']:.1f}", f"Basket: RM {last_row['basket_size_rm']:.2f}")

fig = go.Figure()
colors = {"Shopee MY": "#D92B2B", "Shopee SG": "#1D4ED8", "TikTok MY": "#111111", "TikTok SG": "#EAB308"}
for ch in HYGR_CHANNELS:
    sub = df_m[df_m["platform_region"] == ch]
    fig.add_trace(go.Scatter(x=sub["period"], y=sub["sales_index"], mode="lines+markers", name=f"{ch} Base", line=dict(color=colors[ch], width=2)))
    fig.add_trace(go.Scatter(x=sub["period"], y=sub["macro_predicted_index"], mode="lines", name=f"{ch} Macro Forecast", line=dict(color=colors[ch], dash="dot")))

fig.update_layout(title="HYGR 4-Channel Sales Trajectory (2025-Q1 = 100)", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Private Consumption Macro Drivers (Table 3.5)")
st.dataframe(load_macro_consumption_indicators(), use_container_width=True)
st.subheader("Forecast Matrix Data")
st.dataframe(df_m, use_container_width=True)
