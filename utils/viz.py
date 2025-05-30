import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import json

def plot_kde_by_surgery(df, surgery_group="most", remove_outliers=False, top_n=3):
    if df.empty:
        st.warning("No data available to plot.")
        return

    grouped = df.groupby("surgery")["cases"].sum()
    top_surgeries = (grouped.nlargest(top_n) if surgery_group == "most"
                     else grouped.nsmallest(top_n)).index.tolist()

    plot_df = df[df["surgery"].isin(top_surgeries)].copy()

    if remove_outliers:
        q1 = plot_df["cases"].quantile(0.25)
        q3 = plot_df["cases"].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        plot_df = plot_df[(plot_df["cases"] >= lower) & (plot_df["cases"] <= upper)]

    if plot_df.empty:
        st.warning("No data available after filtering and outlier removal.")
        return

    plt.figure(figsize=(10, 5))
    for surgery in plot_df["surgery"].unique():
        subset = plot_df[plot_df["surgery"] == surgery]
        if subset["cases"].nunique() > 1:
            sns.kdeplot(subset["cases"], fill=True, label=surgery)

    plt.title("KDE Distribution by Surgery Type")
    plt.xlabel("Number of Cases")
    plt.ylabel("Density")
    plt.grid(True, linestyle="--", alpha=0.6)
    # Only show legend if there are any valid labels
    handles, labels = plt.gca().get_legend_handles_labels()
    if labels:
        plt.legend()

    st.pyplot(plt.gcf())
    plt.clf()

def plot_surgery_trends(df, selected_surgeries=None, include_total=True):
    if df.empty:
        st.warning("No data available for trend analysis.")
        return

    trends = df.copy()

    if selected_surgeries:
        trends = trends[trends["surgery"].isin(selected_surgeries)]

    if trends.empty:
        st.warning("No matching surgeries found in selected filters.")
        return

    trends_by_year = trends.groupby(["year", "surgery"])["cases"].sum().reset_index()
    chart_data = trends_by_year.pivot(index="year", columns="surgery", values="cases").fillna(0)

    if include_total:
        chart_data["Filtered Total"] = chart_data.sum(axis=1)

    st.line_chart(chart_data)

def plot_hospital_bubble_map(df):
    # Ensure required columns exist
    if "longitude" not in df.columns or "latitude" not in df.columns:
        st.warning("Location columns are missing from this dataset.")
        return

    # Filter out "Statewide" and rows with missing coordinates
    map_df = df[
        (df["county"].str.lower() != "statewide") &
        df["longitude"].notna() &
        df["latitude"].notna()
    ]

    if map_df.empty:
        st.warning("Location data not available for the current selection.")
        return

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=36.7783,
            longitude=-119.4179,
            zoom=5.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=map_df,
                get_position='[longitude, latitude]',
                get_radius="cases",
                radius_scale=10,
                get_fill_color=[200, 30, 0, 160],
                pickable=True
            )
        ],
        tooltip={"text": "Hospital: {hospital}\nCases: {cases}"}
    ))

def plot_county_choropleth(df, geojson_path="data/ca_counties.geojson"):
    df = df.copy()
    if df.empty:
        st.warning("No data available for county-level map.")
        return

    county_data = df.groupby("county")["cases"].sum().reset_index()
    county_data["county"] = county_data["county"].str.lower()

    try:
        with open(geojson_path, "r") as f:
            geojson = json.load(f)
    except FileNotFoundError:
        st.error("GeoJSON file not found.")
        return

    for feature in geojson["features"]:
        feature["properties"]["name"] = feature["properties"]["name"].lower()

    county_data.columns = ["name", "cases"]
    for feature in geojson["features"]:
        name = feature["properties"]["name"]
        match = county_data[county_data["name"] == name]
        feature["properties"]["cases"] = int(match["cases"].values[0]) if not match.empty else 0

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(latitude=36.5, longitude=-119.5, zoom=5.5),
        layers=[
            pdk.Layer(
                "GeoJsonLayer",
                data=geojson,
                pickable=True,
                stroked=False,
                filled=True,
                get_fill_color="[255 - properties.cases * 2, 100, 100, 150]",
                get_line_color=[0, 0, 0],
                get_line_width=1
            )
        ],
        tooltip={"text": "{name}\nCases: {cases}"}
    ))
