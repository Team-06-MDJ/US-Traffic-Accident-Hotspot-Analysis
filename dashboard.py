import streamlit as st
import pandas as pd
import plotly.express as px
import boto3

# Set page config
st.set_page_config(layout="wide", page_title="US Traffic Accident Analysis")

# Title and Description
st.title("🛣️ US Traffic Accident Analysis (2020-2023)")
st.markdown("""
This dashboard analyzes traffic accident data to identify high-risk hotspots, 
weather impacts, and time-based patterns.
""")

# Constants
DATA_PATH = "s3://us-traffic-accidents-datalake/processed/accidents_2020_2023.parquet"

@st.cache_data
def load_data():
    """
    Load data from S3. Uses caching to avoid reloading on every interaction.
    """
    try:
        # Check if we can access S3, otherwise load a sample or show error
        # For this template, we'll try to read the parquet file directly
        # Ensure you have AWS credentials configured or the bucket is public/accessible
        df = pd.read_parquet(DATA_PATH, engine='pyarrow')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

with st.spinner("Loading data from S3..."):
    df = load_data()

if df is not None:
    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # Year Filter
    if 'Year' in df.columns:
        years = sorted(df['Year'].unique())
        selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
        df_filtered = df[df['Year'] == selected_year]
    else:
        df_filtered = df

    # State Filter (assuming 'State' column exists, if not we can add it or ignore)
    if 'State' in df.columns:
        states = sorted(df['State'].unique())
        selected_state = st.sidebar.multiselect("Select State", states, default=states[:5])
        if selected_state:
            df_filtered = df_filtered[df_filtered['State'].isin(selected_state)]

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Accidents", f"{len(df_filtered):,}")
    
    if 'Severity' in df_filtered.columns:
        avg_severity = df_filtered['Severity'].mean()
        col2.metric("Avg Severity", f"{avg_severity:.2f}")

    # Visualizations
    
    # Map
    st.subheader("📍 Accident Hotspots")
    if 'Start_Lat' in df_filtered.columns and 'Start_Lng' in df_filtered.columns:
        # Sample for map performance if dataset is large
        map_data = df_filtered.sample(min(10000, len(df_filtered))) 
        st.map(map_data, latitude='Start_Lat', longitude='Start_Lng')

    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Accidents by Hour")
        if 'Hour' in df_filtered.columns:
            hourly_counts = df_filtered['Hour'].value_counts().sort_index()
            st.bar_chart(hourly_counts)

    with col_chart2:
        st.subheader("Accidents by Weather Condition")
        if 'Weather_Condition' in df_filtered.columns:
            weather_counts = df_filtered['Weather_Condition'].value_counts().head(10)
            st.bar_chart(weather_counts)

else:
    st.warning("Please ensure the S3 path is correct and you have the necessary AWS permissions.")
