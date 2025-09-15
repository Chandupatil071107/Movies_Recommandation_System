# I added the comments on this file so everyone can understand
import streamlit as st
import pickle
import gdown
import pandas as pd
import requests

# =======================
# Google Drive File IDs (replace with your real IDs!)
# =======================
MOVIES_FILE_ID = "187VPQGkaFYsaqsUFDoxGGrldN-bbFzp8"        # example: 1AbCdEfGh123MOVIESID
SIMILARITY_FILE_ID = "1IOmttRuwby4Awf4X1yLxZBzMvZd5tV51" # example: 1XyZpQrSTUVWXYZSIMILARITY

# =======================
# Download pickle files from Google Drive
# =======================
def download_file(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

download_file(MOVIES_FILE_ID, "movies.pkl")
download_file(SIMILARITY_FILE_ID, "similarity.pkl")

# =======================
# Load Data
# =======================
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# If movies is dict, convert to DataFrame
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

# =======================
# Fetch Poster Function
# =======================
def fetch_poster(movie_id):
    api_key = "YOUR_TMDB_API_KEY"  # Replace with your TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# =======================
# Recommendation Function
# =======================
def recommend(movie):
    if movie not in movies["title"].values:
        return [], []

    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id  # using movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# =======================
# Streamlit UI
# =======================
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie:", movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.error("Movie not found in database!")
