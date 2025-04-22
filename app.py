import pandas as pd
import streamlit as st
import plotly.express as px

# 
st.set_page_config(
    page_title="Netflix Shows🍿",
    page_icon="🍿 ", 
    layout="wide"
)


# 1: Load the dataset
df = pd.read_csv("netflix_titles.csv")

# test for loading dataset
# print(f"Shape: {df.shape}")
# print(df.head())

# 2. Query the dataset
# queried_df = df[df["release_year"] > 2015]

# print(f"Queried_data for release_year > 2015 are:", queried_df.head())



# 3 (i). Building an interactive UI
st.title("Use the Slider to view Netflix movie titles released after threshold 🍿")
# st.dataframe(queried_df, use_container_width=True)

# 3 (ii). adding user controls
# Filter dataset using the selected threshold
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

# sidebar component header
st.sidebar.header("Netflix Dashboard Picks")

# 4. Creating a visualization
year_threshold = st.sidebar.slider(
    "Netflix movie titles released after year:",
    min_value=min_year,
    max_value=max_year,
    value = 2015,
    step = 1
)

queried_df = df[df["release_year"] > year_threshold]

st.subheader(f"Netflix movie titles released after {year_threshold}")
st.dataframe(queried_df, use_container_width=True)

df["duration_extracted"] = df["duration"].str.extract("(\d+)").astype(float)

scatter_data = df.dropna(subset=["release_year", "duration_extracted", "type"])

fig = px.scatter(
    scatter_data, x="release_year", y="duration_extracted", color="type", title="ScatterPlot of Duration of Netflix Movie vs Release Year",
    labels={
        "release_year" : "Release Year", "duration_extracted" : "Duration", "type" : "Movie Type"
    }
)

st.plotly_chart(fig, use_container_width=True)

# additional widgets
# widget 1: filtering by either Movie or TV Show
type_option = st.sidebar.selectbox(
    "Please select the type you'd like to view: ",
    df["type"].dropna().unique()
)

filtered_df = queried_df[queried_df["type"] == type_option]

st.subheader(f"{type_option}s released after {year_threshold}")
st.dataframe(filtered_df, use_container_width=True)

# widget 2: accepting user input by title
search_term = st.sidebar.text_input("Please type the Movie/TV Show Title: ")

if search_term: 
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False, na=False)]

    st.subheader(f"Your search results are: '{search_term}'")
    st.dataframe(filtered_df, use_container_width=True)

