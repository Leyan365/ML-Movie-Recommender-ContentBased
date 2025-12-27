import streamlit as st
import pickle
import pandas as pd
import requests
import os

# -----------------------------------------------------------------------------
# 1. Page Configuration & Aesthetics
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Cinematch | Premium Recommender", layout="wide", page_icon="🎬")

# Custom CSS for Glassmorphism & Dark Mode
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Global Settings */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main Background - Deep Cinematic Gradient */
    .stApp {
        background: radial-gradient(circle at top, #1b2735 0%, #090a0f 100%);
    }

    /* Title Styling */
    .title-text {
        color: #ffffff;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    .subtitle-text {
        color: #b0bac9;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* Card Container Grid */
    .recommendations-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        padding: 20px;
    }

    /* Glassmorphism Card Style */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 15px;
        width: 220px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        color: white;
    }

    .movie-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border-color: rgba(0, 255, 255, 0.3);
    }

    .movie-poster {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    .movie-title {
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Streamlit Input Styling */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    div[data-baseweb="popover"] {
        background-color: #1a1a2e !important;
    }

    div[class*="stSelectbox"] label {
        color: #b0bac9 !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 1.1rem;
        border-radius: 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 210, 255, 0.6);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Logic
# -----------------------------------------------------------------------------
TMDB_API_KEY = os.getenv("API_KEY") # 🔑 TODO: ADD YOUR API KEY HERE

@st.cache_resource
def load_data():
    """Load large datasets only once to improve performance."""
    movies_df = pickle.load(open('movies.pkl', 'rb'))
    similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))
    return movies_df, similarity_matrix

try:
    movies, similarity = load_data()
except FileNotFoundError:
    st.error("Error: 'movies.pkl' or 'similarity.pkl' not found in the directory.")
    st.stop()

import concurrent.futures
import html

def fetch_poster(movie_id):
    """Fetch movie poster URL from TMDB API."""
    if not TMDB_API_KEY:
        # Return a nice placeholder if no key is present
        return "https://via.placeholder.com/500x750/090a0f/ffffff?text=Add+API+Key"
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750/1a1a2e/ffffff?text=No+Poster"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie_title):
    movie_title_lower = movie_title.lower()
    
    # Check if movie exists
    if movie_title_lower not in movies['title'].str.lower().values:
        return None, "Movie not found!"

    movie_index = movies[movies['title'].str.lower() == movie_title_lower].index[0]
    distances = similarity[movie_index]
    # Get top 5 matches (excluding the movie itself at index 0)
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:7]

    recommendations = []
    
    # Helper to fetch data for a single movie
    def get_movie_data(item):
        movie_idx = item[0]
        movie_id = movies.iloc[movie_idx].id
        title = movies.iloc[movie_idx].title
        poster = fetch_poster(movie_id)
        return {"title": title, "poster": poster}

    # Fetch posters in parallel to reduce wait time
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(get_movie_data, movies_list)
        
    recommendations = list(results)
        
    return recommendations, None

# -----------------------------------------------------------------------------
# 3. Application Layout
# -----------------------------------------------------------------------------

# Header
st.markdown('<div class="title-text">🎬 Cinematch</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Discover your next favorite movie with AI-powered recommendations</div>', unsafe_allow_html=True)

# Search Bar
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_name = st.selectbox(
        "Start typing a movie name...",
        movies['title'].values,
        help="Select a movie to get recommendations"
    )

    # Center the button using standard Streamlit columns, layout handled by CSS for style
    if st.button("Get Recommendations"):
        with st.spinner("Finding the best movies for you..."):
            recommendations, error = recommend(selected_movie_name)
        
        if error:
            st.error(error)
        else:
            # Display Results using HTML for maximum styling control
            st.markdown("### Top Picks for You")
            
            # Build HTML string without indentation to avoid Markdown code block parsing
            html_content = '<div class="recommendations-container">'
            for rec in recommendations:
                title_safe = html.escape(rec['title'])
                html_content += f'<div class="movie-card"><img src="{rec["poster"]}" class="movie-poster" alt="{title_safe}"><p class="movie-title" title="{title_safe}">{title_safe}</p></div>'
            html_content += '</div>'
            
            st.markdown(html_content, unsafe_allow_html=True)