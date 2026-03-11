import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="Freshbus Travel Analysis",
    page_icon="🚌",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 18px;
    border-radius: 12px;
}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ======================== DATA LOADING & PREPROCESSING ========================

@st.cache_data
def load_and_preprocess():
    """Load ticket.csv and replicate the notebook preprocessing pipeline."""
    df = pd.read_csv("ticket.csv")

    # --- Route extraction ---
    df["Route"] = df["Service Number"].apply(lambda t: "-".join(t.split("-")[:2]))

    # --- Sleeper / Seater flag ---
    df["isSleeper"] = df["Service Number"].str.contains("SL").astype(int)
    df["Bus Type"] = df["isSleeper"].map({0: "Seater", 1: "Sleeper"})

    # --- Departure time & time bucket ---
    df["Departure Time"] = df["Service Number"].apply(
        lambda t: f"{t.split('-')[-1][:2]}:{t.split('-')[-1][2:]}"
    )

    def time_bucket(t):
        if "05:00" < t <= "09:00":
            return "Early Morning"
        elif "09:00" < t <= "16:00":
            return "Day Service"
        elif "16:00" < t <= "21:00":
            return "Evening"
        return "Overnight"

    df["Time Of Travel"] = df["Departure Time"].apply(time_bucket)

    # --- Datetime conversions ---
    df["Departure Date Time"] = pd.to_datetime(
        df["Journey Date"] + " " + df["Departure Time"], format="mixed"
    )
    df["Booked Date Time"] = pd.to_datetime(df["Booked Date Time"], format="mixed")
    df["Journey Date Time"] = pd.to_datetime(df["Journey Date Time"], format="mixed")

    # --- Booking gap ---
    df["Booking Gap Days"] = (df["Journey Date Time"] - df["Booked Date Time"]).dt.days

    # --- Age groups ---
    df["Age Group"] = pd.cut(
        df["Age"],
        bins=[1, 17, 25, 40, 60, 100],
        labels=["1-17", "18-25", "26-40", "41-60", "60+"],
    )

    # --- Cleanup ---
    df.drop(columns=["Journey Date", "Departure Time"], inplace=True)

    return df


df = load_and_preprocess()

# ======================== SIDEBAR FILTERS ========================
st.sidebar.header("🔎 Filters")

routes = sorted(df["Route"].unique())
categories = sorted(df["Category"].unique())
times = ["Early Morning", "Day Service", "Evening", "Overnight"]
genders = sorted(df["Gender"].unique())
age_groups = ["1-17", "18-25", "26-40", "41-60", "60+"]

sel_routes = st.sidebar.multiselect("Route", routes)
sel_categories = st.sidebar.multiselect("Category", categories)
sel_times = st.sidebar.multiselect("Time of Travel", times)
sel_bus = st.sidebar.multiselect("Bus Type", ["Seater", "Sleeper"])
sel_genders = st.sidebar.multiselect("Gender", genders)
sel_ages = st.sidebar.multiselect("Age Group", age_groups)
fare_range = st.sidebar.slider(
    "Seat Fare Range (₹)",
    int(df["Seat Fare"].min()),
    int(df["Seat Fare"].max()),
    (int(df["Seat Fare"].min()), int(df["Seat Fare"].max())),
)

fdf = df.copy()
if sel_routes:
    fdf = fdf[fdf["Route"].isin(sel_routes)]
if sel_categories:
    fdf = fdf[fdf["Category"].isin(sel_categories)]
if sel_times:
    fdf = fdf[fdf["Time Of Travel"].isin(sel_times)]
if sel_bus:
    fdf = fdf[fdf["Bus Type"].isin(sel_bus)]
if sel_genders:
    fdf = fdf[fdf["Gender"].isin(sel_genders)]
if sel_ages:
    fdf = fdf[fdf["Age Group"].astype(str).isin(sel_ages)]
fdf = fdf[(fdf["Seat Fare"] >= fare_range[0]) & (fdf["Seat Fare"] <= fare_range[1])]

n = len(fdf)

# ======================== HEADER ========================
st.title("🚌 Freshbus — Travel & Booking Analysis Dashboard")
st.caption("Interactive dashboard based on the Freshbus ticket dataset")

# ======================== KPI CARDS ========================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Tickets", f"{n:,}")
k2.metric("Avg Fare", f"₹{fdf['Seat Fare'].mean():,.0f}" if n else "—")
k3.metric("Total Revenue", f"₹{fdf['Total Ticket Amount'].sum():,.0f}" if n else "—")
k4.metric("Unique Routes", fdf["Route"].nunique())
k5.metric("Avg Booking Gap", f"{fdf['Booking Gap Days'].mean():.1f} days" if n else "—")

if n == 0:
    st.warning("No data matches the current filters. Adjust filters in the sidebar.")
    st.stop()

# ======================== TAB LAYOUT ========================
tab_overview, tab_routes, tab_demographics, tab_booking, tab_data = st.tabs(
    ["📊 Overview", "🛣️ Route Analysis", "👥 Demographics", "🕐 Booking Behaviour", "📋 Data"]
)

# ------------------------------------------------------------------ #
# TAB 1 — OVERVIEW
# ------------------------------------------------------------------ #
with tab_overview:
    st.subheader("Bus Type Preference (Seater vs Sleeper)")
    c1, c2 = st.columns(2)
    with c1:
        bus_counts = fdf["Bus Type"].value_counts().reset_index()
        bus_counts.columns = ["Bus Type", "Bookings"]
        fig = px.pie(bus_counts, names="Bus Type", values="Bookings",
                     hole=0.45, color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(margin=dict(t=30, b=30))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(bus_counts, x="Bus Type", y="Bookings",
                     color="Bus Type", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Seat Fare Distribution")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(fdf, x="Seat Fare", nbins=40, marginal="box",
                           color_discrete_sequence=["#667eea"])
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.box(fdf, y="Seat Fare", color="Bus Type",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Bookings by Time of Travel")
    time_counts = fdf["Time Of Travel"].value_counts().reindex(times).reset_index()
    time_counts.columns = ["Time Of Travel", "Bookings"]
    fig = px.bar(time_counts, x="Time Of Travel", y="Bookings",
                 color="Time Of Travel", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------ #
# TAB 2 — ROUTE ANALYSIS
# ------------------------------------------------------------------ #
with tab_routes:
    st.subheader("Top 10 Routes by Ticket Count")
    top10 = fdf["Route"].value_counts().head(10).reset_index()
    top10.columns = ["Route", "Tickets"]
    fig = px.bar(top10, x="Route", y="Tickets", color="Tickets",
                 color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Revenue by Route × Category
    st.subheader("Revenue by Route & Category")
    rev_rc = fdf.groupby(["Route", "Category"])["Total Ticket Amount"].sum().reset_index()
    fig = px.bar(rev_rc, x="Route", y="Total Ticket Amount", color="Category",
                 barmode="group", color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Revenue by Route × Time of Travel
    st.subheader("Revenue by Route & Time of Travel")
    rev_rt = fdf.groupby(["Route", "Time Of Travel"])["Total Ticket Amount"].sum().reset_index()
    fig = px.bar(rev_rt, x="Route", y="Total Ticket Amount", color="Time Of Travel",
                 barmode="group", color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Heatmaps
    st.subheader("Revenue Heatmap — Route × Time of Travel")
    pivot_rev = pd.pivot_table(fdf, values="Total Ticket Amount",
                               index="Route", columns="Time Of Travel", aggfunc="sum").fillna(0)
    fig = px.imshow(pivot_rev, text_auto=".0f", color_continuous_scale="YlOrRd", aspect="auto")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Booking Volume Heatmap — Route × Time of Travel")
    pivot_cnt = pd.pivot_table(fdf, values="Ticket No",
                               index="Route", columns="Time Of Travel", aggfunc="count").fillna(0)
    fig = px.imshow(pivot_cnt, text_auto=".0f", color_continuous_scale="Viridis", aspect="auto")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------ #
# TAB 3 — DEMOGRAPHICS
# ------------------------------------------------------------------ #
with tab_demographics:
    st.subheader("Bookings by Age Group")
    c1, c2 = st.columns(2)
    with c1:
        age_counts = fdf["Age Group"].value_counts().sort_index().reset_index()
        age_counts.columns = ["Age Group", "Bookings"]
        fig = px.bar(age_counts, x="Age Group", y="Bookings",
                     color="Age Group", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        gender_counts = fdf["Gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Bookings"]
        fig = px.pie(gender_counts, names="Gender", values="Bookings",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set1,
                     title="Bookings by Gender")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Age Group × Category
    st.subheader("Age Group Distribution Across Categories")
    age_cat = fdf.groupby(["Category", "Age Group"], observed=False).size().reset_index(name="Count")
    fig = px.bar(age_cat, x="Category", y="Count", color="Age Group",
                 barmode="group", color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Gender × Time of Travel
    st.subheader("Gender-wise Travel Time Preference")
    gen_time = fdf.groupby(["Gender", "Time Of Travel"]).size().reset_index(name="Bookings")
    fig = px.bar(gen_time, x="Time Of Travel", y="Bookings", color="Gender",
                 barmode="group", color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Gender × Time × Age stacked
    st.subheader("Gender Booking Pattern by Time & Age Group")
    gen_time_age = (
        fdf.groupby(["Gender", "Time Of Travel", "Age Group"], observed=False)
        .size()
        .reset_index(name="Bookings")
    )
    c1, c2 = st.columns(2)
    for col_widget, g in zip([c1, c2], sorted(fdf["Gender"].unique())):
        with col_widget:
            sub = gen_time_age[gen_time_age["Gender"] == g]
            fig = px.bar(sub, x="Time Of Travel", y="Bookings", color="Age Group",
                         title=f"Gender: {g}", barmode="stack",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------ #
# TAB 4 — BOOKING BEHAVIOUR
# ------------------------------------------------------------------ #
with tab_booking:
    st.subheader("Booking Gap Distribution (Days)")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(fdf, x="Booking Gap Days", nbins=30, marginal="violin",
                           color_discrete_sequence=["#764ba2"])
        fig.update_layout(bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.box(fdf, x="Category", y="Booking Gap Days", color="Category",
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Category × Time of Travel revenue
    st.subheader("Revenue by Category & Time of Travel")
    cat_time = fdf.groupby(["Category", "Time Of Travel"])["Total Ticket Amount"].sum().reset_index()
    fig = px.bar(cat_time, x="Category", y="Total Ticket Amount", color="Time Of Travel",
                 barmode="group", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Fare vs Total Amount scatter
    st.subheader("Seat Fare vs Total Ticket Amount")
    fig = px.scatter(fdf, x="Seat Fare", y="Total Ticket Amount",
                     color="Category", hover_data=["Route", "Bus Type"],
                     opacity=0.6, color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Strategic insights
    st.subheader("🧠 Strategic Insights")
    top_route = fdf["Route"].mode().iloc[0]
    top_time = fdf["Time Of Travel"].mode().iloc[0]
    dominant_gender = fdf["Gender"].mode().iloc[0]
    dominant_age = fdf["Age Group"].mode().iloc[0]
    multi_seat_pct = (fdf["Total Ticket Amount"] > fdf["Seat Fare"]).mean() * 100
    avg_gap = fdf["Booking Gap Days"].mean()

    st.markdown(f"""
| Insight | Detail |
|---------|--------|
| **Most Booked Route** | {top_route} |
| **Peak Travel Time** | {top_time} |
| **Dominant Gender** | {dominant_gender} |
| **Most Active Age Group** | {dominant_age} |
| **Multi-seat Bookings** | {multi_seat_pct:.1f}% |
| **Avg Booking Gap** | {avg_gap:.1f} days |
""")

# ------------------------------------------------------------------ #
# TAB 5 — DATA EXPLORER
# ------------------------------------------------------------------ #
with tab_data:
    st.subheader("Filtered Dataset")
    st.dataframe(fdf, use_container_width=True, height=500)
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered CSV", data=csv,
                       file_name="filtered_bus_data.csv", mime="text/csv")
