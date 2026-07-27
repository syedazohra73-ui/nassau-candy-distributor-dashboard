import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Nassau Candy Distributor Dashboard",
    page_icon="🍬",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#f8fafc;
}

h1{
    color:#0f172a;
    text-align:center;
    font-weight:bold;
}

h2,h3{
    color:#1e3a8a;
}

div[data-testid="metric-container"]{
    background:#ffffff;
    border:2px solid #dbeafe;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

section[data-testid="stSidebar"]{
    background:#eff6ff;
}

.stButton>button{
    background:#2563eb;
    color:white;
    border-radius:10px;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_excel("Route_Summary.xlsx")

# -----------------------------
# Header
# -----------------------------
st.markdown("""
# 🍬 Nassau Candy Distributor Dashboard

### 📊 Shipping Route & Distribution Analytics

Analyze shipping routes, monitor factory performance,
compare state-wise orders and support logistics decisions.

---
""")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🔎 Dashboard Filter")

factory = st.sidebar.multiselect(
    "Select Factory",
    sorted(df["Factory"].unique()),
    default=sorted(df["Factory"].unique())
)

filtered_df = df[df["Factory"].isin(factory)]

# -----------------------------
# KPI Cards
# -----------------------------
col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "📦 Total Orders",
        f"{filtered_df['Orders'].sum():,}"
    )

with col2:
    st.metric(
        "🚚 Total Routes",
        len(filtered_df)
    )

with col3:
    st.metric(
        "🏭 Active Factories",
        filtered_df["Factory"].nunique()
    )

st.divider()

# -----------------------------
# Charts
# -----------------------------
left,right = st.columns(2)

with left:

    st.subheader("🏭 Orders by Factory")

    factory_orders = (
        filtered_df.groupby("Factory")["Orders"]
        .sum()
        .sort_values(ascending=False)
    )

    fig = px.bar(
        x=factory_orders.index,
        y=factory_orders.values,
        labels={"x":"Factory","y":"Orders"},
        color=factory_orders.values,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("🥧 Factory Order Distribution")

    fig = px.pie(
        filtered_df,
        names="Factory",
        values="Orders",
        hole=.45
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Orders by State
# -----------------------------
st.subheader("📍 Orders by State")

state_orders = (
    filtered_df.groupby("State/Province")["Orders"]
    .sum()
    .sort_values(ascending=False)
)

fig = px.bar(
    x=state_orders.index,
    y=state_orders.values,
    labels={"x":"State","y":"Orders"},
    color=state_orders.values,
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Route Summary
# -----------------------------
st.subheader("📋 Route Summary")

st.dataframe(filtered_df, use_container_width=True)

# -----------------------------
# Download Button
# -----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name="Filtered_Route_Summary.csv",
    mime="text/csv"
)

st.divider()

# -----------------------------
# Factory Performance
# -----------------------------
st.subheader("🏆 Factory Performance")

performance = (
    filtered_df.groupby("Factory")["Orders"]
    .sum()
    .sort_values(ascending=False)
)

st.table(performance)

st.divider()

# -----------------------------
# Project Summary
# -----------------------------
st.subheader("📌 Project Summary")

st.markdown("""
This dashboard helps businesses to:

✅ Monitor shipping performance

✅ Compare factory-wise order distribution

✅ Analyze state-wise demand

✅ Improve logistics planning

✅ Support supply chain decision making

### Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- Microsoft Excel
""")

st.divider()

st.success("✔ Dashboard Developed Successfully")

st.caption("Developed by Arbeen | BCA Data Analytics Project")
st.caption("Nassau Candy Distributor Dashboard")