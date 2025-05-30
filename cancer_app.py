import streamlit as st
from utils.load import load_cancer_data
from utils.filters import get_filter_controls
from utils.viz import (
    plot_kde_by_surgery,
    plot_surgery_trends,
    plot_hospital_bubble_map,
    plot_county_choropleth
)

# --- Page Setup ---
st.set_page_config(
    page_title="Surgical Scope",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Global Style Block ---
STYLE_BLOCK = """
<style>
    h1 {
        font-size: 2.3rem !important;
        margin-bottom: 0.5rem;
    }
    h3 {
        font-size: 1.5rem !important;
        margin-top: 2rem;
    }
    .section-note {
        font-size: 1rem;
        color: #555;
        margin-top: 0;
        max-width: 800px;
    }
    .footer {
        font-size: 0.85rem;
        color: #777;
        text-align: center;
        padding-top: 40px;
        margin-top: 30px;
    }
</style>
"""
st.markdown(STYLE_BLOCK, unsafe_allow_html=True)

# --- App Header ---
st.markdown("""
    <h1>Surgical Scope: Cancer Procedure Trends in California</h1>
    <p class='section-note'>
        This interactive application visualizes cancer surgery data from California hospitals between 2013 and 2022. 
        Use filters to explore regional trends, compare procedure volumes over time, and view hospital-level or county-level distribution maps for 11 common cancer surgeries.
    </p>
""", unsafe_allow_html=True)

# --- Load and Filter Data ---
df = load_cancer_data()
filters = get_filter_controls(df)

filtered_df = df[
    (df["year"].isin(filters["years"])) &
    (df["surgery"].isin(filters["surgeries"])) &
    (df["county"].isin(filters["regions"]))
]

# --- Tabbed Layout ---
tab1, tab2, tab3 = st.tabs(["🔍 Overview", "📊 Visualizations", "💾 Export"])

# --- Tab 1: Overview ---
with tab1:
    st.markdown("### 📋 Overview")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### Filtered Records")
        cols_to_drop = [col for col in ["LONGITUDE", "LATITUDE", "longitude", "latitude"] if col in filtered_df.columns]
       # Remove LONG/LAT only for the overview table when showing "Statewide"
        overview_df = filtered_df.copy()
        if "Statewide" in filters["regions"]:
            overview_df = overview_df.drop(columns=["LONGITUDE", "LATITUDE"], errors="ignore")

        st.dataframe(overview_df.head(), use_container_width=True)

    with col2:
        st.markdown("#### Summary Stats")
        total_cases = filtered_df["cases"].sum()
        top_surgery = (
            filtered_df.groupby("surgery")["cases"]
            .sum()
            .sort_values(ascending=False)
            .idxmax()
            if not filtered_df.empty else "N/A"
        )
        hospital_count = filtered_df["hospital"].nunique()

        st.metric("Total Surgeries", f"{total_cases:,}")
        st.metric("Top Surgery Type", top_surgery)
        st.metric("Hospitals Represented", hospital_count)

# --- Tab 2: Visualizations ---
with tab2:
    st.markdown("### 📊 Interactive Visualizations")

    with st.expander("🎛️ View KDE Distribution Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            group_choice = st.radio(
                "Surgery Group",
                options=["most", "least"],
                index=0,
                format_func=lambda x: "Most Common" if x == "most" else "Least Common"
            )
        with col2:
            outlier_toggle = st.checkbox("Remove Outliers", value=False)
        with col3:
            top_n = st.slider("Number of Surgery Types", 1, 5, value=3)

        st.markdown("##### Surgery Type Distribution (KDE)")
        plot_kde_by_surgery(
            filtered_df,
            surgery_group=group_choice,
            remove_outliers=outlier_toggle,
            top_n=top_n
        )

    with st.expander("📈 View Surgery Volume Trends", expanded=True):
        surgery_options = sorted(filtered_df["surgery"].unique())
        selected_surgeries = st.multiselect(
            "Select Surgery Types to Display",
            options=surgery_options,
            default=surgery_options[:3]
        )
        show_total = st.checkbox("Include Total Line", value=True)

        if not selected_surgeries and show_total:
            plot_surgery_trends(filtered_df, selected_surgeries=[], include_total=True)
        elif selected_surgeries:
            plot_surgery_trends(filtered_df, selected_surgeries, include_total=show_total)

    st.markdown("#### 📍 Location Visualizations")

    map_mode = st.radio(
        "Choose Map Type:",
        options=["None", "Hospital Bubble Map", "County Choropleth Map"],
        index=0,
        horizontal=True
    )

if map_mode == "Hospital Bubble Map":
    plot_hospital_bubble_map(filtered_df)

elif map_mode == "County Choropleth Map":
    plot_county_choropleth(filtered_df, geojson_path="data/ca_counties.geojson")


# --- Tab 3: Export ---
with tab3:
    st.markdown("### 💾 Export Filtered Data")

    st.markdown(
        "You can download the currently filtered dataset as a CSV file. "
        "This can be used for further analysis or sharing."
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="filtered_cancer_surgeries.csv",
        mime="text/csv"
    )

    st.markdown("### 📝 Methodology Notes")
    st.info(
        "This dataset comes from California's HCAI open data portal. "
        "It includes 11 surgery types from 2013–2022. Use caution when comparing 2015 due to ICD coding changes."
    )

# --- Footer ---
st.markdown("<hr class='footer'><div class='footer'>📈 Built with Streamlit • Data Source: California HCAI • © 2025 Alexis Parker</div>", unsafe_allow_html=True)
