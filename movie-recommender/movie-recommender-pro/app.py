import streamlit as st
import pickle
import pandas as pd
import requests
import os

# 1. Poster fetch karne ka function
def fetch_poster(movie_id):
    # YAHAN APNI API KEY DAALEIN
    api_key = "2baef23b1ff0355934e527b513aa1d3a"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# 2. Files ke raaste (Paths) set karna
current_dir = os.path.dirname(__file__)
movie_dict_path = os.path.join(current_dir, 'notebooks', 'movie_dict.pkl')
similarity_path = os.path.join(current_dir, 'notebooks', 'similarity.pkl')

# 3. Data Load karna (Error handling ke saath)
try:
    movies_dict = pickle.load(open(movie_dict_path, 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open(similarity_path, 'rb'))
except FileNotFoundError:
    st.error(f"Files nahi mili! Check karein ki '{movie_dict_path}' aur '{similarity_path}' GitHub par hain ya nahi.")
    st.stop()

# 4. Recommendation Logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_posters

# 5. Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search for a movie you liked:',
    movies['title'].values
)

if st.button('Show Recommendations'):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie_name)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])