import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.templates.default = "plotly_white"

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
    background: linear-gradient(135deg,#2563eb,#1d4ed8);
    padding:20px;
    border-radius:18px;
    color:white;
    box-shadow:0 8px 20px rgba(0,0,0,.18);
    border:none;
}

div[data-testid="metric-container"] label{
    color:white !important;
    font-weight:bold;
    font-size:16px;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"]{
    color:white !important;
    font-size:30px;
    font-weight:700;
}

section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#eff6ff,#dbeafe);
    border-right:2px solid #bfdbfe;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_excel("Nassau Candy Distributor.xlsx")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
# -----------------------------
# Dashboard Title
# -----------------------------
# -----------------------------
# Dashboard Title
# -----------------------------

st.markdown("""
<h1 style="text-align:center;color:#1E3A8A;font-size:48px;font-weight:bold;">
🍬 Nassau Candy Distributor Dashboard
</h1>

<h3 style="text-align:center;color:#64748B;">
Business Intelligence & Supply Chain Analytics
</h3>

<p style="text-align:center;font-size:18px;color:#475569;">
Analyze sales, distribution, shipping performance, regional demand, and business insights in one interactive dashboard.
</p>

<hr>
""", unsafe_allow_html=True)

st.divider()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Dashboard Filters")

# Date Range Filter
start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max().date()
)

# Region Filter
region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

# Division Filter
division = st.sidebar.multiselect(
    "Division",
    options=sorted(df["Division"].dropna().unique()),
    default=sorted(df["Division"].dropna().unique())
)

# Ship Mode Filter
ship_mode = st.sidebar.multiselect(
    "Ship Mode",
    options=sorted(df["Ship Mode"].dropna().unique()),
    default=sorted(df["Ship Mode"].dropna().unique())
)

# Apply Filters
filtered_df = df[
    (df["Order Date"] >= pd.to_datetime(start_date)) &
    (df["Order Date"] <= pd.to_datetime(end_date)) &
    (df["Region"].isin(region)) &
    (df["Division"].isin(division)) &
    (df["Ship Mode"].isin(ship_mode))
]

st.divider()
# -----------------------------
# Business KPIs
# -----------------------------

total_sales = filtered_df["Sales"].sum()
total_units = filtered_df["Units"].sum()
gross_profit = filtered_df["Gross Profit"].sum()
total_cost = filtered_df["Cost"].sum()

profit_margin = (
    (gross_profit / total_sales) * 100
    if total_sales > 0 else 0
)

average_order_value = (
    total_sales / filtered_df["Order ID"].nunique()
    if filtered_df["Order ID"].nunique() > 0 else 0
)

top_state = (
    filtered_df.groupby("State/Province")["Sales"]
    .sum()
    .idxmax()
    if not filtered_df.empty else "N/A"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("📦 Total Units", f"{int(total_units):,}")

with col3:
    st.metric("💵 Gross Profit", f"${gross_profit:,.2f}")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("💸 Total Cost", f"${total_cost:,.2f}")

with col5:
    st.metric("📈 Profit Margin", f"{profit_margin:.2f}%")

with col6:
    st.metric("🏆 Top State", top_state)

st.divider()
# -----------------------------
# Monthly Sales & Profit Trends
# -----------------------------

monthly_data = filtered_df.copy()
monthly_data["Month"] = monthly_data["Order Date"].dt.to_period("M").astype(str)

monthly_summary = (
    monthly_data.groupby("Month")[["Sales", "Gross Profit"]]
    .sum()
    .reset_index()
)

left, right = st.columns(2)

with left:

    st.subheader("📅 Monthly Sales Trend")

    fig = px.line(
        monthly_summary,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales"
    )

    fig.update_layout(
        title_x=0.5,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        title_font_size=22,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

   st.subheader("📅 Monthly Profit Trend")

fig = px.line(
    monthly_summary,
    x="Month",
    y="Gross Profit",
    markers=True,
    title="Monthly Gross Profit"
)

fig.update_layout(
    title_x=0.5,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

# =====================================================
# Sales by Region & State
# =====================================================

left, right = st.columns(2)

# -----------------------------
# Sales by Region
# -----------------------------
with left:

   st.subheader("🌎 Sales by Region")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Sales",
    color_continuous_scale="Blues",
    text_auto=".2s",
    title="Sales by Region"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Sales",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Sales by State
# -----------------------------
with right:

    st.subheader("📍 Sales by State")

state_sales = (
    filtered_df.groupby("State/Province")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig = px.bar(
    state_sales,
    x="State/Province",
    y="Sales",
    color="Sales",
    color_continuous_scale="Viridis",
    text_auto=".2s",
    title="Sales by State"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="State",
    yaxis_title="Sales",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
# =====================================================
# Sales by Division & Ship Mode Analysis
# =====================================================

left, right = st.columns(2)

# -----------------------------
# Sales by Division
# -----------------------------
with left:

    st.subheader("🥧 Sales by Division")

division_sales = (
    filtered_df.groupby("Division")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    division_sales,
    names="Division",
    values="Sales",
    hole=0.50,
    title="Sales Distribution by Division"
)

fig.update_layout(
    title_x=0.5,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    legend_title="Division",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Ship Mode Analysis
# -----------------------------
with right:

    st.subheader("🚚 Ship Mode Analysis")

ship_sales = (
    filtered_df.groupby("Ship Mode")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    ship_sales,
    x="Ship Mode",
    y="Sales",
    color="Sales",
    color_continuous_scale="Plasma",
    text_auto=".2s",
    title="Sales by Ship Mode"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Ship Mode",
    yaxis_title="Sales",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
# -----------------------------
# Top 10 Products
# -----------------------------
left, right = st.columns(2)

with left:

   st.subheader("🍫 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    color_continuous_scale="Blues",
    text_auto=".2s",
    title="Top 10 Products by Sales"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Sales",
    yaxis_title="Product",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20),
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top 10 Customers
# -----------------------------
with right:

    st.subheader("👤 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer ID")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customers,
    x="Customer ID",
    y="Sales",
    color="Sales",
    color_continuous_scale="Greens",
    text_auto=".2s",
    title="Top 10 Customers by Sales"
)

fig.update_layout(
    title_x=0.5,
    xaxis_title="Customer ID",
    yaxis_title="Sales",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)
st.divider()

# -----------------------------
# Interactive Data Table
# -----------------------------
st.subheader("📋 Filtered Sales Data")

st.dataframe(
    filtered_df,
    width="stretch",
    height=500
)

st.divider()
# -----------------------------
# Sales by State Map
# -----------------------------
st.subheader("🗺️ Sales by State (USA Map)")

state_map = (
    filtered_df.groupby("State/Province")["Sales"]
    .sum()
    .reset_index()
)

fig = px.choropleth(
    state_map,
    locations="State/Province",
    locationmode="USA-states",
    color="Sales",
    scope="usa",
    color_continuous_scale="Blues",
    hover_name="State/Province",
    hover_data={"Sales": ":,.2f"}
)

fig.update_layout(
    title="Sales Distribution Across States",
    title_x=0.5,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=14),
    title_font_size=22,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
# =====================================================
# Download Buttons
# =====================================================

st.subheader("📥 Download Filtered Data")

# CSV Download
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="Filtered_Sales.csv",
    mime="text/csv"
)

# Excel Download
filtered_df.to_excel("Filtered_Sales.xlsx", index=False)

with open("Filtered_Sales.xlsx", "rb") as file:
    st.download_button(
        label="⬇ Download Excel",
        data=file,
        file_name="Filtered_Sales.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.divider()

# =====================================================
# Project Summary
# =====================================================

st.subheader("📌 Project Summary")

st.markdown("""
### 🚀 Business Intelligence Dashboard Features

✅ Interactive Date Range Filter

✅ Region Filter

✅ Ship Mode Filter

✅ Division Filter

✅ Real-Time KPI Cards

✅ Monthly Sales Trend

✅ Monthly Profit Trend

✅ Sales by Region

✅ Sales by State

✅ Sales by Division

✅ Ship Mode Analysis

✅ Top Products Analysis

✅ Download Filtered Data (CSV & Excel)

---

### 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express
- Microsoft Excel

---

This dashboard helps monitor sales, logistics, distribution performance, and business insights using interactive visualizations.
""")

st.divider()

# =====================================================
# Professional Footer
# =====================================================

st.markdown("---")

footer = """
<div style="
    background: linear-gradient(90deg,#2563eb,#1e40af);
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
">

<h2>🍬 Nassau Candy Distributor Dashboard</h2>

<h4>Business Intelligence & Sales Analytics Dashboard</h4>

<hr style="border:1px solid rgba(255,255,255,0.3);">

<p>
📊 Interactive Analytics |
📈 Real-Time KPIs |
📦 Sales Insights |
🚚 Distribution Analytics
</p>

<p>
Developed using ❤️ Python • Streamlit • Pandas • Plotly
</p>

</div>
"""

st.markdown(footer, unsafe_allow_html=True)

st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("💰 Total Sales Analysis")

with col2:
    st.success("📦 Distribution Insights")

with col3:
    st.warning("📈 Business Intelligence")

st.markdown("---")

st.caption("© 2026 Nassau Candy Distributor Dashboard")
st.caption("Developed by Syeda Zohra | BCA Data Analytics Project")
