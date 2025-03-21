import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv('StudentsPerformance.csv')

st.title("Students Performance Dashboard")

st.markdown("""
This dashboard allows you to explore the dataset through various visualizations:
- **Univariate Analysis:** Histograms for exam scores and bar charts for categorical features.
- **Bivariate Analysis:** Scatter plots and box plots comparing different scores and categorical groups.
- **Multivariate Analysis:** Scatter matrix, correlation heatmap, and parallel coordinates plots.
Use the sidebar to filter the data interactively.
""")

# --- Sidebar for Filtering ---
st.sidebar.header("Filters")

# Filter for categorical features
gender_options = df['gender'].unique().tolist()
selected_genders = st.sidebar.multiselect("Select Gender", options=gender_options, default=gender_options)

race_options = df['race/ethnicity'].unique().tolist()
selected_races = st.sidebar.multiselect("Select Race/Ethnicity", options=race_options, default=race_options)

parental_options = df['parental level of education'].unique().tolist()
selected_parental = st.sidebar.multiselect("Select Parental Level of Education", options=parental_options, default=parental_options)

lunch_options = df['lunch'].unique().tolist()
selected_lunch = st.sidebar.multiselect("Select Lunch Type", options=lunch_options, default=lunch_options)

test_prep_options = df['test preparation course'].unique().tolist()
selected_test_prep = st.sidebar.multiselect("Select Test Preparation Course", options=test_prep_options, default=test_prep_options)

# Filter for numerical features using slider widgets
math_min, math_max = int(df['math score'].min()), int(df['math score'].max())
math_range = st.sidebar.slider("Math Score Range", math_min, math_max, (math_min, math_max))

reading_min, reading_max = int(df['reading score'].min()), int(df['reading score'].max())
reading_range = st.sidebar.slider("Reading Score Range", reading_min, reading_max, (reading_min, reading_max))

writing_min, writing_max = int(df['writing score'].min()), int(df['writing score'].max())
writing_range = st.sidebar.slider("Writing Score Range", writing_min, writing_max, (writing_min, writing_max))

# Apply filters to the DataFrame
filtered_df = df[
    (df['gender'].isin(selected_genders)) &
    (df['race/ethnicity'].isin(selected_races)) &
    (df['parental level of education'].isin(selected_parental)) &
    (df['lunch'].isin(selected_lunch)) &
    (df['test preparation course'].isin(selected_test_prep)) &
    (df['math score'] >= math_range[0]) & (df['math score'] <= math_range[1]) &
    (df['reading score'] >= reading_range[0]) & (df['reading score'] <= reading_range[1]) &
    (df['writing score'] >= writing_range[0]) & (df['writing score'] <= writing_range[1])
]

st.write("### Filtered Data Summary")
st.write(f"Total records: {filtered_df.shape[0]}")

# --- Tabs for Different Visualizations ---
tabs = st.tabs(["Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis", "Data Table"])

# Univariate Analysis
with tabs[0]:
    st.header("Univariate Analysis")
    
    # Histograms for exam scores
    fig1 = px.histogram(filtered_df, x="math score", nbins=20, title="Distribution of Math Scores")
    st.plotly_chart(fig1, use_container_width=True)
    
    fig2 = px.histogram(filtered_df, x="reading score", nbins=20, title="Distribution of Reading Scores")
    st.plotly_chart(fig2, use_container_width=True)
    
    fig3 = px.histogram(filtered_df, x="writing score", nbins=20, title="Distribution of Writing Scores")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Bar charts for categorical features
    categorical_cols = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
    for col in categorical_cols:
        fig = px.histogram(filtered_df, x=col, title=f"Count of {col}")
        st.plotly_chart(fig, use_container_width=True)

# Bivariate Analysis
with tabs[1]:
    st.header("Bivariate Analysis")
    
    # Scatter plots for score relationships
    fig4 = px.scatter(filtered_df, x="math score", y="reading score", color="gender",
                        title="Math vs. Reading Score")
    st.plotly_chart(fig4, use_container_width=True)
    
    fig5 = px.scatter(filtered_df, x="math score", y="writing score", color="test preparation course",
                        title="Math vs. Writing Score")
    st.plotly_chart(fig5, use_container_width=True)
    
    fig6 = px.scatter(filtered_df, x="reading score", y="writing score", color="race/ethnicity",
                        title="Reading vs. Writing Score")
    st.plotly_chart(fig6, use_container_width=True)
    
    # Box plots to compare distributions
    fig7 = px.box(filtered_df, x="gender", y="math score", title="Math Score Distribution by Gender")
    st.plotly_chart(fig7, use_container_width=True)
    
    fig8 = px.box(filtered_df, x="lunch", y="reading score", title="Reading Score Distribution by Lunch Type")
    st.plotly_chart(fig8, use_container_width=True)

# Multivariate Analysis
with tabs[2]:
    st.header("Multivariate Analysis")
    
    # Scatter matrix (pair plot)
    fig9 = px.scatter_matrix(filtered_df,
                             dimensions=["math score", "reading score", "writing score"],
                             color="gender",
                             title="Scatter Matrix of Exam Scores")
    st.plotly_chart(fig9, use_container_width=True)
    
    # Correlation heatmap
    corr = filtered_df[["math score", "reading score", "writing score"]].corr()
    fig10 = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
    st.plotly_chart(fig10, use_container_width=True)
    
    # Parallel coordinates plot for multivariate trends
    fig11 = px.parallel_coordinates(filtered_df,
                                    dimensions=["math score", "reading score", "writing score"],
                                    color="math score",
                                    title="Parallel Coordinates Plot")
    st.plotly_chart(fig11, use_container_width=True)

# Data Table for direct inspection
with tabs[3]:
    st.header("Data Table")
    st.dataframe(filtered_df)
