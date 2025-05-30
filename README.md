## Surgical Scope: Cancer Procedure Trends in California

[![Streamlit App](https://img.shields.io/badge/launch-app-brightgreen)](https://surgical-scope.streamlit.app)

A responsive web app for exploring statewide trends in cancer surgery volumes across California hospitals from 2013 to 2022. Built for clarity and accessibility, the app allows users to filter by county, year, and surgery type while comparing distributions, trends over time, and hospital locations across 11 procedure categories.

## Launch the App

Access the deployed version here: [surgical-scope.streamlit.app](https://surgical-scope.streamlit.app)

> **Note:** The live version of this app is optimized for performance using a streamlined dataset.  
> For full functionality and complete data access, clone the repository and run the app locally using the instructions below.

## Key Features

This Streamlit app provides an interactive, filterable view of cancer surgery trends based on public data from the California Department of Health Care Access and Information (HCAI). Core features include:

- **Dynamic Filtering:** Explore by county, year range, and specific surgery types.
- **Distribution Comparisons:** Visualize the most and least common cancer procedures using KDE plots, with an option to remove statistical outliers.
- **Volume Trends:** Generate line charts to observe year-over-year case volumes, including overlays for total surgeries and selected procedures.
- **Geographic View:** Display hospitals by location and filter scope.
- **CSV Download:** Export a filtered subset of the dataset for additional offline analysis.

All visualizations are styled for accessibility, interpretability, and ethical data presentation.

## Local Setup

To run the app locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/cancer-deploy.git
    cd cancer-deploy
    ```

2. **(Optional) Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**

    ```bash
    streamlit run cancer_app.py
    ```

Once launched, the app will open automatically in your browser at `http://localhost:8501`.

## App Usage

Once launched, the app opens to a clean, tab-based interface organized as follows:

### Overview Tab
- View summary statistics and preview the filtered dataset in table format.
- Apply filters for county, year, and surgery type using the sidebar.

### Visualizations Tab
- **KDE Plots:** Compare distributions of the most and least common surgeries, with an option to remove outliers.
- **Trend Charts:** Plot selected surgery types over time alongside total volumes.
- **Hospital Map:** Optionally display locations of hospitals performing surgeries in the filtered dataset.

### Export Tab
- Download the current filtered dataset as a CSV file for offline use or further analysis.

The app supports real-time interactivity, accessible design, and clear presentation across devices and screen sizes.

## Repository Structure

The project is organized for clarity and modular development. Each component supports reusability and ease of maintenance.

```text
cancer-deploy/
├── cancer_app.py            # Main Streamlit app script
├── data/
│   └── surgeries.csv        # Cleaned cancer surgeries dataset
├── utils/                   # Modular utility components
│   ├── __init__.py
│   ├── load.py              # Data loading
│   ├── filters.py           # Sidebar controls
│   ├── prep.py              # Data preparation and transformation
│   └── viz.py               # Visualizations and plotting functions
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
└── requirements.txt         # Python dependencies
```

The app runs entirely from local files to ensure consistent behavior during deployment. No external APIs or cloud services are required. Each module is structured to promote transparency, reproducibility, and ease of extension as future datasets or visualizations are added.
