# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
#
#
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=911cacf195339d794ed68996943ab157"
#     response = requests.get(url)
#     data = response.json()
#     poster_path = data.get('poster_path')  # extract poster path
#     if poster_path:
#         return "https://image.tmdb.org/t/p/w500" + poster_path
#     else:
#         return "https://via.placeholder.com/500x750?text=No+Image"  # fallback if poster not found
#
#
#
#
# def recommand(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     recommended_movies=[]
#     recommended_movies_posters=[]
#     for i in movies_list:
#         movie_id=movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_posters
#
#
# movies_dict=pickle.load(open('movie_dict.pkl','rb'))
# movies=pd.DataFrame(movies_dict)
#
# similarity=pickle.load(open('similarity.pkl','rb'))
# st.title('Movie Recommander System')
#
#
#
#
#
#
# selected_movie_name = st.selectbox(
#     "Choose a movie to get similar recommendations:",
#     movies['title'].values,
# )
# if st.button('Recommand'):
#     names,posters=recommand(selected_movie_name)
#     col1,col2,col3,col4,col5=st.columns(5)
#     with col1:
#         st.header(names[0])
#         st.image(posters[0])
#
#     with col2:
#         st.header(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.header(names[2])
#         st.image(posters[2])
#
#     with col4:
#         st.header(names[3])
#         st.image(posters[3])
#
#     with col5:
#         st.header(names[4])
#         st.image(posters[4])
#
# # st.write("You selected:", option)










#
# #--->
#
#
# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
#
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=911cacf195339d794ed68996943ab157"
#     try:
#         response = requests.get(url, timeout=10)  # add timeout
#         response.raise_for_status()  # raise error if bad status
#         data = response.json()
#         poster_path = data.get('poster_path')
#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500" + poster_path
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Image"
#     except requests.exceptions.RequestException as e:
#         st.error(f"Error fetching poster for movie_id {movie_id}: {e}")
#         return "https://via.placeholder.com/500x750?text=Error"
#
#
# def recommand(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies, recommended_movies_posters
#
#
# # Load pickles
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# # Streamlit UI
# st.title('🎬 Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     "Choose a movie to get similar recommendations:",
#     movies['title'].values,
# )
#
# if st.button('Recommend'):
#     names, posters = recommand(selected_movie_name)
#     cols = st.columns(5)
#     for idx, col in enumerate(cols):
#         with col:
#             st.text(names[idx])
#             st.image(posters[idx])








# OMDB API KEY
# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import time
#
#
# # ---------------------- Fetch Poster Function ----------------------
# def fetch_poster(movie_title):
#     api_key = "e39708f0"  # your OMDb API key
#     url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
#
#     for attempt in range(3):  # try up to 3 times
#         try:
#             response = requests.get(url, timeout=30)  # increased timeout
#             response.raise_for_status()
#             data = response.json()
#
#             # Check if poster exists
#             poster_url = data.get("Poster")
#             if poster_url and poster_url != "N/A":
#                 return poster_url
#             else:
#                 return "https://via.placeholder.com/500x750?text=No+Image"
#
#         except requests.exceptions.RequestException as e:
#             if attempt < 2:
#                 time.sleep(2)  # wait before retry
#                 continue
#             return "https://via.placeholder.com/500x750?text=Error"
#
#
# # ---------------------- Recommender Function ----------------------
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)),
#                          reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_posters = []
#
#     for i in movies_list:
#         title = movies.iloc[i[0]].title
#         recommended_movies.append(title)
#         recommended_posters.append(fetch_poster(title))
#
#     return recommended_movies, recommended_posters
#
#
# # ---------------------- Load Data ----------------------
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# # ---------------------- Streamlit UI ----------------------
# st.title('🎬 Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     "Choose a movie to get similar recommendations:",
#     movies['title'].values
# )
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#
#     cols = st.columns(5)
#     for idx, col in enumerate(cols):
#         with col:
#             st.subheader(names[idx])
#             st.image(posters[idx])







# After adding a style to the background
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
    api_key = "e39708f0"  # your OMDb API key
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
                    <div class="movie-info">📅 {year}</div>
                    <div class="movie-info">🎭 {genre}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
