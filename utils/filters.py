import streamlit as st

def get_filter_controls(df):
    st.markdown("### 🎛️ Filter Your View")

    # Unique values for filters
    all_years = sorted(df["year"].dropna().unique())
    all_surgeries = sorted(df["surgery"].dropna().unique())
    
    # Replace and reorder counties (now called regions)
    df["county"] = df["county"].replace("Statewide", "California (Statewide)")
    all_regions = sorted(df["county"].dropna().unique().tolist())
    if "California (Statewide)" in all_regions:
        all_regions.remove("California (Statewide)")
        all_regions = ["California (Statewide)"] + all_regions

    # Filters - inline layout with columns
    col1, col2, col3 = st.columns(3)

    with col1:
        years = st.multiselect(
            "Select Year(s)",
            options=all_years,
            default=all_years,
            help="Select one or more years to explore"
        )

    with col2:
        surgeries = st.multiselect(
            "Select Surgery Type(s)",
            options=all_surgeries,
            default=["Breast", "Colon", "Prostate", "Esophagus", "Pancreas", "Stomach"],
            help="Select one or more types of cancer surgeries"
        )

    with col3:
        regions = st.multiselect(
            "Select Region(s)",
            options=all_regions,
            default=["Los Angeles"],
            help="Includes both counties and California-wide data"
        )

    return {
        "years": years,
        "surgeries": surgeries,
        "regions": regions
    }
