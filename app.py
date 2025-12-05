import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import s3fs

# ============================================================
# DARK THEME PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="US Traffic Accident Dashboard",
    layout="wide",
    page_icon="🚗",
    initial_sidebar_state="expanded"
)

# Dark theme CSS
st.markdown("""
    <style>
        body, .main, .block-container {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
        h1, h2, h3, h4, h5, h6, label, .stMarkdown {
            color: #fafafa !important;
        }
        .stMetric {
            background-color: #1b1f27 !important;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 US Traffic Accident Analytics Dashboard")
st.markdown("### Interactive analytics for US Traffic Accidents (2020–2023)")


# ============================================================
# LOAD PARQUET FROM S3 BY YEAR
# ============================================================

import s3fs   # add this near the top with other imports

# ---------- Replace your existing load_data_by_years function with this ----------
fs = s3fs.S3FileSystem()

@st.cache_data(show_spinner=True)
def load_data_by_years(selected_years):
    """
    Loads the single Parquet file from S3 using s3fs to avoid PyArrow S3 HEAD issues.
    Filters by year after loading (cheap compared to re-reading).
    """
    path = "s3://us-traffic-accidents-datalake/processed/accidents_2020_2023_50pct.parquet"


    # Open with s3fs to ensure streaming and avoid HeadObject metadata errors
    with fs.open(path, "rb") as f:
        df = pd.read_parquet(f, engine="pyarrow")

    # Ensure timestamp columns are parsed
    if "start_time" in df.columns:
        df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    if "end_time" in df.columns:
        df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")

    # Optional: drop rows with no coords (speed up downstream)
    if {"start_lat", "start_lng"}.issubset(df.columns):
        df = df.dropna(subset=["start_lat", "start_lng"])

    # Filter by selected years (if provided)
    if selected_years:
        # make sure 'year' exists and is integer-like
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
            df = df[df["year"].isin(selected_years)]
        else:
            # fallback: derive year from start_time if available
            if "start_time" in df.columns:
                df["year"] = df["start_time"].dt.year
                df = df[df["year"].isin(selected_years)]

    return df

# ============================================================
# FILTERS
# ============================================================
st.sidebar.header("🎛 Filters")

ALL_YEARS = [2020, 2021, 2022, 2023]

selected_years = st.sidebar.multiselect(
    "Select Year(s):",
    options=ALL_YEARS,
    default=[]
)

if not selected_years:
    st.warning("👈 Please select one or more years from the sidebar.")
    st.stop()

with st.spinner("⏳ Loading data from S3 (optimized parquet partitions)..."):
    df = load_data_by_years(selected_years)

st.success(f"Loaded {len(df):,} records for years {selected_years}")

df.columns = df.columns.str.lower()

df["start_time"] = pd.to_datetime(df["start_time"], errors="ignore")
df["end_time"] = pd.to_datetime(df["end_time"], errors="ignore")
df["response_minutes"] = (df["end_time"] - df["start_time"]).dt.total_seconds() / 60
df["response_minutes"] = df["response_minutes"].clip(lower=0, upper=120)


state_filter = st.sidebar.selectbox(
    "Filter by State:",
    ["All"] + sorted(df["state"].dropna().unique().tolist())
)

severity_filter = st.sidebar.multiselect(
    "Severity Levels:",
    sorted(df["severity"].dropna().unique()),
    default=sorted(df["severity"].dropna().unique())
)

hour_range = st.sidebar.slider("Hour Range:", 0, 23, (0, 23))

filtered_df = df.copy()
if state_filter != "All":
    filtered_df = filtered_df[filtered_df["state"] == state_filter]

filtered_df = filtered_df[filtered_df["severity"].isin(severity_filter)]
filtered_df = filtered_df[
    (filtered_df["hour"] >= hour_range[0]) &
    (filtered_df["hour"] <= hour_range[1])
]

st.success(f"Filtered Rows: {len(filtered_df):,}")


# ============================================================
# KPI METRICS
# ============================================================
st.markdown("## 🔍 Summary Metrics")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Accidents", f"{len(filtered_df):,}")
k2.metric("Unique States", filtered_df["state"].nunique())
k3.metric("Most Common Severity", int(filtered_df["severity"].mode().iloc[0]))
k4.metric("Avg Response Time (min)", round(filtered_df["response_minutes"].mean(), 2))


# ============================================================
# INTERACTIVE HOTSPOT MAP (FOLIUM)
# ============================================================
st.markdown("## 🗺️ Accident Hotspot Map")

map_df = filtered_df.sample(min(3000, len(filtered_df)))

m = folium.Map(
    location=[map_df["start_lat"].mean(), map_df["start_lng"].mean()],
    zoom_start=4,
    tiles="CartoDB dark_matter"   # DARK THEME MAP
)

marker_cluster = MarkerCluster().add_to(m)

for _, row in map_df.iterrows():
    folium.CircleMarker(
        location=[row["start_lat"], row["start_lng"]],
        radius=4,
        color="#ff4d4d",
        fill=True,
        fill_color="#ff4d4d",
        fill_opacity=0.6,
        popup=f"""
            <b>City:</b> {row['city']}<br>
            <b>State:</b> {row['state']}<br>
            <b>Severity:</b> {row['severity']}
        """,
    ).add_to(marker_cluster)

st_folium(m, width=1400, height=550)


# ============================================================
# PLOTLY USA CHOROPLETH (NO GEOPANDAS)
# ============================================================
st.markdown("## 🇺🇸 State-Level Choropleth Map")

state_counts = filtered_df.groupby("state").size().reset_index(name="count")

us_state_abbrev = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO',
    'Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID',
    'Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
    'Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN',
    'Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
    'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC',
    'North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA',
    'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX',
    'Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV',
    'Wisconsin':'WI','Wyoming':'WY'
}

# Convert names → abbreviations if needed
if state_counts["state"].str.len().max() > 2:
    state_counts["state"] = state_counts["state"].map(us_state_abbrev)

fig_choro = px.choropleth(
    state_counts,
    locations="state",
    locationmode="USA-states",
    color="count",
    color_continuous_scale="reds",
    scope="usa",
    title="Accident Density by State"
)
st.plotly_chart(fig_choro, use_container_width=True)


# ============================================================
# TIME TRENDS
# ============================================================
st.markdown("## 📈 Time Trends")

colA, colB = st.columns(2)

monthly = filtered_df.groupby("month").size().reset_index(name="count")
fig_month = px.line(monthly, x="month", y="count", markers=True,
                    title="Accidents Per Month")
colA.plotly_chart(fig_month, use_container_width=True)

dow = filtered_df.groupby("dayofweek").size().reset_index(name="count")
fig_dow = px.bar(dow, x="dayofweek", y="count",
                 title="Accidents By Day of Week")
colB.plotly_chart(fig_dow, use_container_width=True)


# ============================================================
# ACCIDENT HEATMAP
# ============================================================
st.markdown("## 🔥 Accident Heatmap (Hour × Day)")

heat = filtered_df.value_counts(["dayofweek", "hour"]).reset_index(name="count")
pivot = heat.pivot(index="dayofweek", columns="hour", values="count").fillna(0)

fig_heat = px.imshow(
    pivot,
    labels={"x": "Hour", "y": "Day", "color": "Accidents"},
    aspect="auto",
    color_continuous_scale="inferno"
)
st.plotly_chart(fig_heat, use_container_width=True)


# ============================================================
# RESPONSE TIME
# ============================================================
st.markdown("## 🚑 Response Time Distribution")

fig_resp = px.histogram(
    filtered_df,
    x="response_minutes",
    nbins=40,
    title="Response Time (Minutes)"
)
st.plotly_chart(fig_resp, use_container_width=True)


# ============================================================
# WEATHER CONDITIONS
# ============================================================
st.markdown("## 🌦 Weather Condition Impact")

weather_counts = filtered_df["weather_condition"].value_counts().head(10)
fig_weather = px.bar(
    weather_counts,
    title="Top Weather Conditions in Accidents",
    labels={"value": "Count", "index": "Weather Condition"}
)
st.plotly_chart(fig_weather, use_container_width=True)
