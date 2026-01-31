import streamlit as st
import pickle
import pandas as pd
import requests

# 1. Poster fetch karne ka function (Pehle define karna zaroori hai)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2baef23b1ff0355934e527b513aa1d3a&language=en-US"
    try:
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        # Agar poster na mile toh ye placeholder image dikhayega
        return "https://via.placeholder.com/500x750?text=No+Poster"

# 2. Data Load karein
movies_dict = pickle.load(open('notebooks/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('notebooks/similarity.pkl', 'rb'))

# 3. Recommendation logic jo posters bhi return karega
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id  # 'id' column se TMDB ID uthayega
        recommended_movies.append(movies.iloc[i[0]].title)
        # Poster fetch function ko call kar rahe hain
        recommended_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_posters

# 4. Streamlit UI Design
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search for a movie you liked:',
    movies['title'].values
)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    
    # 5 Columns layout banane ke liye
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