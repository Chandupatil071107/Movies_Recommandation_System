# I added the comments on this file so everyone can understand
import streamlit as st
import pandas as pd
import requests
import pickle
import time

# ---------------------- Streamlit Custom CSS ----------------------
st.markdown("""
    <style>
    .stApp {
        background: url("https://www.transparenttextures.com/patterns/cubes.png"), linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-size: cover;
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    h1 { text-align: center; color: #ffcc00; font-size: 3rem; margin-bottom: 20px; text-shadow: 3px 3px 8px #000; }
    h3 { text-align: center; color: #ffffff; font-size: 1.3rem; margin-bottom: 30px; font-weight: 400; }
    .movie-card { background: rgba(255,255,255,0.08); border-radius: 15px; padding: 15px; text-align: center; transition:0.3s; backdrop-filter: blur(6px); }
    .movie-card:hover { transform: scale(1.08); background: rgba(255,255,255,0.18); box-shadow:0 8px 20px rgba(0,0,0,0.5); }
    .movie-title { font-size:1.1rem; font-weight:bold; color:#ffcc00; margin-top:10px; text-shadow:1px 1px 4px #000; }
    .movie-info { font-size:0.9rem; color:#ddd; margin-top:5px; }
    .stButton button { background-color:#ff4757; color:white; border-radius:10px; padding:10px 25px; font-size:1rem; transition:0.3s; border:none; box-shadow:0px 4px 10px rgba(0,0,0,0.4); }
    .stButton button:hover { background-color:#e84118; transform:scale(1.05); }
    .stSelectbox div[data-baseweb="select"] { background-color:white; color:black; border-radius:10px; padding:5px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Google Drive File IDs ----------------------
MOVIE_DICT_ID = "187VPQGkaFYsaqsUFDoxGGrldN-bbFzp8"
SIMILARITY_ID  = "1IOmttRuwby4Awf4X1yLxZBzMvZd5tV51"

# ---------------------- Load Pickle Files from Google Drive ----------------------
@st.cache_data
def load_pickle_from_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    return pickle.loads(response.content)

movies_dict = load_pickle_from_drive(MOVIE_DICT_ID)
movies = pd.DataFrame(movies_dict)
similarity = load_pickle_from_drive(SIMILARITY_ID)

# ---------------------- Fetch Movie Info from OMDb ----------------------
@st.cache_data
def fetch_movie_data(movie_title):
    api_key = st.secrets["omdb"]["api_key"]  # OMDb API key from Streamlit secrets
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=20)
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
                time.sleep(1)
                continue
            return "https://via.placeholder.com/500x750?text=Error", "N/A", "N/A", "N/A"

# ---------------------- Recommendation Function ----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_data = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster, year, genre, plot = fetch_movie_data(title)
        recommended_data.append((title, poster, year, genre, plot))

    return recommended_data

# ---------------------- Streamlit UI ----------------------
st.title('🎬 Movie Recommender System')
st.markdown("<h3>Find similar movies based on your favorite one!</h3>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Choose a movie:",
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
                    <div class="movie-info">📅 {year}</div>
                    <div class="movie-info">🎭 {genre}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
