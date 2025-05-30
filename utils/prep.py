import pandas as pd

def get_common_surgeries(df, top_n=3):
    """
    Returns the most and least common surgeries based on total volume.
    """
    totals = df.groupby("surgery")["cases"].sum()
    most_common = totals.nlargest(top_n).index.tolist()
    least_common = totals.nsmallest(top_n).index.tolist()
    return most_common, least_common

def is_plot_ready(series, min_points=3, require_variance=True):
    """
    Determines if a Series is suitable for KDE or line plotting.
    - min_points: minimum number of data points required
    - require_variance: if True, excludes flat-value groups
    """
    if len(series) < min_points:
        return False
    if require_variance and series.nunique() == 1:
        return False
    return True
