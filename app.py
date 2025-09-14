# I added the comments on this file so everyone can understand
import streamlit as st
import pickle
import pandas as pd
import requests
import time

# ---------------------- Custom CSS ----------------------
st.markdown("""
    <style>
    /* Background with a cinema-style wallpaper */
    .stApp {
        background: url("https://www.transparenttextures.com/patterns/cubes.png"), linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-size: cover;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    /* Title */
    h1 {
        text-align: center;
        color: #ffcc00;
        font-size: 3rem;
        margin-bottom: 20px;
        text-shadow: 3px 3px 8px #000000;
    }

    /* Subtitle */
    h3 {
        text-align: center;
        color: #ffffff;
        font-size: 1.3rem;
        margin-bottom: 30px;
        font-weight: 400;
    }

    /* Movie Cards */
    .movie-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: 0.3s;
        backdrop-filter: blur(6px);
    }
    .movie-card:hover {
        transform: scale(1.08);
        background: rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }

    /* Movie Titles */
    .movie-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #ffcc00;
        margin-top: 10px;
        text-shadow: 1px 1px 4px #000;
    }

    /* Movie Info */
    .movie-info {
        font-size: 0.9rem;
        color: #ddd;
        margin-top: 5px;
    }

    /* Buttons */
    .stButton button {
        background-color: #ff4757;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 1rem;
        transition: 0.3s;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }
    .stButton button:hover {
        background-color: #e84118;
        transform: scale(1.05);
    }

    /* Dropdown */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white;
        color: black;
        border-radius: 10px;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)


# ---------------------- Fetch Poster Function ----------------------
def fetch_movie_data(movie_title):
    api_key = "e39708f0"  
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            poster_url = data.get("Poster")
            year = data.get("Year", "N/A")
            genre = data.get("Genre", "N/A")
            plot = data.get("Plot", "N/A")

            if not poster_url or poster_url == "N/A":
                poster_url = "https://via.placeholder.com/500x750?text=No+Image"

            return poster_url, year, genre, plot

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(2)
                continue
            return "https://via.placeholder.com/500x750?text=Error", "N/A", "N/A", "N/A"


# ---------------------- Recommender Function ----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]

    recommended_data = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster, year, genre, plot = fetch_movie_data(title)
        recommended_data.append((title, poster, year, genre, plot))

    return recommended_data


# ---------------------- Load Data ----------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------- Streamlit UI ----------------------
st.title('🎬 Movie Recommender System')
st.markdown("<h3>Find similar movies based on your favorite one!</h3>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Choose a movie to get similar recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            title, poster, year, genre, plot = recommendations[idx]
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" width="150" style="border-radius:10px;">
                    <div class="movie-title">{title}</div>
                    <div class="movie-info">{year}</div>
                    <div class="movie-info">{genre}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
