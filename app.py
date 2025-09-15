# I added the comments on this file so everyone can understand
import streamlit as st
import pickle
import pandas as pd
import requests

# ------------------- CONFIG -------------------
OMDB_API_KEY = "e39708f0"  # your OMDb key
MOVIES_FILE_ID = "187VPQGkaFYsaqsUFDoxGGrldN-bbFzp8"
SIMILARITY_FILE_ID = "1IOmttRuwby4Awf4X1yLxZBzMvZd5tV51"

# ------------------- GOOGLE DRIVE LOADER -------------------
@st.cache_resource
def load_pickle_from_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    return pickle.loads(requests.get(url).content)

movies = load_pickle_from_drive(MOVIES_FILE_ID)
similarity = load_pickle_from_drive(SIMILARITY_FILE_ID)
movies = pd.DataFrame(movies)

# ------------------- POSTER FETCHER -------------------
def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster = data.get("Poster")
    if poster and poster != "N/A":
        return poster
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

# ------------------- RECOMMENDER -------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))
    return recommended_movie_names, recommended_movie_posters

# ------------------- UI DESIGN -------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            margin-bottom: 50px;
            color: #ddd;
        }
        .movie-card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-radius: 15px;
            overflow: hidden;
            text-align: center;
            padding: 10px;
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(8px);
        }
        .movie-card:hover {
            transform: scale(1.08);
            box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        }
        .movie-card img {
            border-radius: 12px;
            height: 350px;
            object-fit: cover;
            margin-bottom: 10px;
        }
        .movie-title {
            font-size: 16px;
            font-weight: bold;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- MAIN APP -------------------
st.markdown("<div class='title'>🎬 Movie Recommendation System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Discover your next favorite movie</div>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend 🎥"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[idx]}" width="100%">
                    <div class="movie-title">{names[idx]}</div>
                </div>
            """, unsafe_allow_html=True)
