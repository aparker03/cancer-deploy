import pandas as pd
import streamlit as st

@st.cache_data
def load_cancer_data():
    # Load the raw data
    df = pd.read_csv("data/surgeries.csv", encoding="latin1")

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Rename for clarity
    df.rename(columns={"#_of_cases": "cases"}, inplace=True)

    # Drop rows where surgery or year is missing (if any)
    df.dropna(subset=["surgery", "year"], inplace=True)

    # Ensure types
    df["cases"] = df["cases"].astype(int)
    df["year"] = df["year"].astype(int)

    # Normalize casing
    df["surgery"] = df["surgery"].str.title()
    df["hospital"] = df["hospital"].str.title()
    if "county" in df.columns:
        df["county"] = df["county"].fillna("Statewide").str.title()

    return df
