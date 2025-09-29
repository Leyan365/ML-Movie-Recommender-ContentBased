import streamlit as st
import pickle
import pandas as pd
import requests

# Load processed data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB poster fetcher
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY_HERE&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except:
        return "https://via.placeholder.com/300x450?text=Error"

# Recommendation logic
def recommend(movie):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return [], [], f"❌ Movie '{movie}' not found in dataset."

    idx = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[idx]))
    movies_sorted = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movies_sorted:
        movie_id = movies.iloc[i[0]].id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters, None

# UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Search or select a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    with st.spinner("Fetching recommendations... please wait ⏳"):
        titles, posters, error = recommend(selected_movie)

    if error:
        st.error(error)
    else:
        st.subheader("Top 5 Recommendations:")
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(titles[i])
