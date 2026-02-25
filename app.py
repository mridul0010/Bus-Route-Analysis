import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Bus Travel EDA Dashboard", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Updated Key Metrics styling: grey background and black text */
    .stMetric {
        background-color: #ADADAD !important;
        color: #000000 !important;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Ensure label and value within metric are also black */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚌 Bus Travel Data — EDA Dashboard")
st.write("Interactive Analysis of Routes, Ticket Categories, and Fare Trends")

# ================= LOAD DATA =================
@st.cache_data
def load_data(file_source="Final_bus.csv"):
    if os.path.exists(file_source):
        try:
            df = pd.read_csv(file_source)
            # Ensure numeric conversion for fare columns
            if "Seat Fare" in df.columns:
                df["Seat Fare"] = pd.to_numeric(df["Seat Fare"], errors='coerce').fillna(0)
            if "Total Ticket Amount" in df.columns:
                df["Total Ticket Amount"] = pd.to_numeric(df["Total Ticket Amount"], errors='coerce').fillna(0)
            return df
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
            return None
    else:
        st.error(f"File not found: `{file_source}`. Please ensure the file is placed in the same directory as this script.")
        return None

# Automatically load the data without prompting the user
df_raw = load_data()

# Stop the app gracefully if the dataset isn't found
if df_raw is None:
    st.stop()

# ================= STATIC COLUMN MAPPING =================
COLUMN_MAP = {
    "Encode Route": "Route",
    "Category": "Category",
    "Time Of Travel": "Time_of_Travel",
    "Seat Fare": "Seat Fare",
    "Total Ticket Amount": "Total_Amount",
    "Gender": "Gender",
    "Age Group": "Age_Group"
}

# Rename for internal logic - only renames columns that exist in df_raw
df = df_raw.copy().rename(columns=COLUMN_MAP)

# Ensure required columns exist after renaming to avoid calculation errors
required_cols = ["Route", "Category", "Time_of_Travel", "Seat Fare", "Total_Amount", "Gender", "Age_Group"]
for col in required_cols:
    if col not in df.columns:
        df[col] = "N/A" if col not in ["Seat Fare", "Total_Amount"] else 0

# ================= FILTERS =================
st.sidebar.header("🔎 Filters")

route_filter = st.sidebar.multiselect("Select Route", sorted(df["Route"].unique()))
category_filter = st.sidebar.multiselect("Select Category", sorted(df["Category"].unique()))
time_filter = st.sidebar.multiselect("Select Time of Travel", sorted(df["Time_of_Travel"].unique()))
gender_filter = st.sidebar.multiselect("Select Gender", sorted(df["Gender"].astype(str).unique()))
age_filter = st.sidebar.multiselect("Select Age Group", sorted(df["Age_Group"].astype(str).unique()))

filtered_df = df.copy()

if route_filter:
    filtered_df = filtered_df[filtered_df["Route"].isin(route_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]
if time_filter:
    filtered_df = filtered_df[filtered_df["Time_of_Travel"].isin(time_filter)]
if gender_filter:
    filtered_df = filtered_df[filtered_df["Gender"].isin(gender_filter)]
if age_filter:
    filtered_df = filtered_df[filtered_df["Age_Group"].isin(age_filter)]

# ================= KPI CARDS =================
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

# Handle empty dataframe cases to prevent 'NaN'
total_tickets = len(filtered_df)
avg_fare = filtered_df['Seat Fare'].mean() if total_tickets > 0 else 0
total_rev = filtered_df['Total_Amount'].sum() if total_tickets > 0 else 0
max_book = filtered_df['Total_Amount'].max() if total_tickets > 0 else 0

with col1:
    st.metric("Total Tickets", f"{total_tickets:,}")
with col2:
    st.metric("Avg Seat Fare", f"₹{round(float(avg_fare), 2)}")
with col3:
    st.metric("Total Revenue", f"₹{round(float(total_rev), 2):,}")
with col4:
    st.metric("Max Booking", f"₹{round(float(max_book), 2):,}")

# ================= REVENUE & FARE ANALYSIS =================
st.divider()
c1, c2 = st.columns(2)

if total_tickets > 0:
    with c1:
        st.subheader("💺 Category: Seat Fare vs Total Amount")
        cat_means = filtered_df.groupby("Category")[["Seat Fare", "Total_Amount"]].mean().reset_index()
        fig1 = px.bar(cat_means, x="Category", y=["Seat Fare", "Total_Amount"], 
                     barmode='group', color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("🛣️ Top 10 Routes by Revenue")
        route_rev = filtered_df.groupby("Route")["Total_Amount"].sum().sort_values(ascending=False).head(10).reset_index()
        fig2 = px.bar(route_rev, x="Route", y="Total_Amount", color="Total_Amount", color_continuous_scale='Viridis')
        st.plotly_chart(fig2, use_container_width=True)

    # ================= DEMOGRAPHICS & CORRELATION =================
    st.divider()
    d1, d2 = st.columns(2)

    with d1:
        st.subheader("👥 Demographic Distribution")
        demo_tab1, demo_tab2 = st.tabs(["Age Group Revenue", "Gender Distribution"])
        
        with demo_tab1:
            age_gen_rev = filtered_df.groupby(["Age_Group", "Gender"])["Total_Amount"].sum().reset_index()
            fig3 = px.bar(age_gen_rev, x="Age_Group", y="Total_Amount", color="Gender", barmode="group")
            st.plotly_chart(fig3, use_container_width=True)
        
        with demo_tab2:
            gender_counts = filtered_df["Gender"].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
            fig_pie = px.pie(gender_counts, values="Count", names="Gender", 
                             hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)

    with d2:
        st.subheader("🎯 Seat Fare vs Transaction Total")
        fig4 = px.scatter(filtered_df, x="Seat Fare", y="Total_Amount", color="Category", 
                         hover_data=["Route"], opacity=0.6)
        st.plotly_chart(fig4, use_container_width=True)

    # ================= HEATMAP =================
    st.divider()
    st.subheader("🔥 Route × Time Volume Heatmap")
    top_10 = filtered_df["Route"].value_counts().nlargest(10).index
    heatmap_data = filtered_df[filtered_df["Route"].isin(top_10)]

    if not heatmap_data.empty:
        pivot = pd.pivot_table(heatmap_data, values="Total_Amount", index="Route", 
                               columns="Time_of_Travel", aggfunc="count").fillna(0)
        fig_map, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(pivot, annot=True, fmt='g', cmap="YlGnBu", ax=ax)
        st.pyplot(fig_map)
    else:
        st.info("Filter selection is too narrow for a heatmap.")

    # ================= DYNAMIC INSIGHTS =================
    st.divider()
    st.subheader("🧠 Strategic Insights")

    top_route = filtered_df["Route"].mode().values[0] if not filtered_df["Route"].empty else "N/A"
    top_time = filtered_df["Time_of_Travel"].mode().values[0] if not filtered_df["Time_of_Travel"].empty else "N/A"
    dominant_gender = filtered_df["Gender"].mode().values[0] if not filtered_df["Gender"].empty else "N/A"
    multi_seat_perc = (filtered_df["Total_Amount"] > filtered_df["Seat Fare"]).mean() * 100
    
    st.markdown(f"""
    - **Operational Lead:** The most frequently booked route is **{top_route}**, with peak travel during **{top_time}**.
    - **Customer Profile:** Passengers are predominantly **{dominant_gender}**, with the **{filtered_df['Age_Group'].mode().values[0] if not filtered_df['Age_Group'].empty else 'N/A'}** age bracket being the most active.
    - **Group Travel:** Approximately **{multi_seat_perc:.1f}%** of bookings are for multiple seats (where Total Amount > Seat Fare).
    - **Yield:** The average transaction value is **₹{avg_fare:.2f}**, supported by a max transaction of **₹{max_book}**.
    """)

else:
    st.warning("No data matches the selected filters. Please adjust your criteria.")

# ================= DOWNLOAD =================
if total_tickets > 0:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered CSV", data=csv, file_name="filtered_bus_data.csv", mime="text/csv")
