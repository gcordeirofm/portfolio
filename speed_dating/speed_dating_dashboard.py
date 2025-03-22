import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Speed Dating Data Explorer", layout="wide")

@st.cache
def load_data():
    # Adjust the path as needed if the CSV is in a different location.
    df = pd.read_csv("Speed Dating Data.csv", encoding='ISO-8859-1')
    return df

# Load the dataset
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")

# Gender filter (if the gender column is categorical)
if "gender" in df.columns:
    genders = df["gender"].unique()
    selected_genders = st.sidebar.multiselect("Select Gender", options=genders, default=genders)
    df = df[df["gender"].isin(selected_genders)]

# Age filter
if "age" in df.columns:
    min_age = int(df["age"].min())
    max_age = int(df["age"].max())
    age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))
    df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]

# Race filter (if available)
if "race" in df.columns:
    races = df["race"].unique()
    selected_races = st.sidebar.multiselect("Select Race", options=races, default=races)
    df = df[df["race"].isin(selected_races)]

# Field of Study filter (if available)
if "field" in df.columns:
    fields = df["field"].unique()
    selected_fields = st.sidebar.multiselect("Select Field of Study", options=fields, default=fields)
    df = df[df["field"].isin(selected_fields)]

# Visualization selector
st.sidebar.header("Visualization Options")
viz_option = st.sidebar.selectbox("Choose a visualization", 
                                  options=["Data Table", "Summary Statistics", "Univariate Analysis", 
                                           "Bivariate Analysis", "Correlation Heatmap", "Box Plot"])

st.title("Speed Dating Data Explorer")
st.write("Explore the Speed Dating dataset with interactive visualizations.")

# Option: Data Table
if viz_option == "Data Table":
    st.subheader("Data Table")
    st.dataframe(df)

# Option: Summary Statistics
elif viz_option == "Summary Statistics":
    st.subheader("Summary Statistics")
    st.write(df.describe(include="all"))

# Option: Univariate Analysis (Histogram)
elif viz_option == "Univariate Analysis":
    st.subheader("Univariate Analysis")
    # Select a numeric column for histogram
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        col = st.selectbox("Select a numeric column", options=numeric_cols)
        bins = st.slider("Number of bins", min_value=5, max_value=100, value=20)
        
        # Using Altair for an interactive histogram
        chart = alt.Chart(df).mark_bar().encode(
            alt.X(f"{col}:Q", bin=alt.Bin(maxbins=bins), title=col),
            y='count()'
        ).properties(width=700, height=400, title=f"Histogram of {col}")
        st.altair_chart(chart)
    else:
        st.write("No numeric columns available for univariate analysis.")

# Option: Bivariate Analysis (Scatter Plot)
elif viz_option == "Bivariate Analysis":
    st.subheader("Bivariate Analysis")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Select X-axis", options=numeric_cols, index=0)
        y_axis = st.selectbox("Select Y-axis", options=numeric_cols, index=1)
        color_option = None
        # Optionally color by a categorical variable if available
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if cat_cols:
            color_option = st.selectbox("Color by (optional)", options=[None] + cat_cols, index=0)
        
        chart = alt.Chart(df).mark_circle(size=60).encode(
            x=alt.X(x_axis, title=x_axis),
            y=alt.Y(y_axis, title=y_axis),
            tooltip=numeric_cols,
            color=color_option if color_option else alt.value("steelblue")
        ).interactive().properties(width=700, height=400, title=f"{y_axis} vs {x_axis}")
        st.altair_chart(chart)
    else:
        st.write("Not enough numeric columns for bivariate analysis.")

# Option: Correlation Heatmap
elif viz_option == "Correlation Heatmap":
    st.subheader("Correlation Heatmap")
    # Compute correlation matrix on numeric features
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()

    # Use Altair's heatmap style
    corr = corr.reset_index().melt('index')
    heatmap = alt.Chart(corr).mark_rect().encode(
        x=alt.X('variable:N', title='Variable'),
        y=alt.Y('index:N', title='Variable'),
        color=alt.Color('value:Q', scale=alt.Scale(scheme='blueorange'), title='Correlation'),
        tooltip=['index', 'variable', 'value']
    ).properties(width=700, height=700, title="Correlation Heatmap")
    st.altair_chart(heatmap)

# Option: Box Plot Analysis
elif viz_option == "Box Plot":
    st.subheader("Box Plot Analysis")
    # Let user choose a numeric column and a categorical column for grouping
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if numeric_cols and cat_cols:
        num_col = st.selectbox("Select a numeric column", options=numeric_cols)
        cat_col = st.selectbox("Select a categorical column for grouping", options=cat_cols)
        
        # Create a box plot using Altair
        boxplot = alt.Chart(df).mark_boxplot(extent='min-max').encode(
            x=alt.X(f"{cat_col}:N", title=cat_col),
            y=alt.Y(f"{num_col}:Q", title=num_col),
            color=alt.Color(f"{cat_col}:N")
        ).properties(width=700, height=400, title=f"Box Plot of {num_col} grouped by {cat_col}")
        st.altair_chart(boxplot)
    else:
        st.write("Insufficient numeric or categorical columns for box plot analysis.")

# Additional interactive features could be added here as needed.
