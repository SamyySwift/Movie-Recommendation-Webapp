import streamlit as st
import pickle
import requests
from functions import *

api_key = "5a3e8d796d7e3539c7aefeff6b5c26cd"

st.set_page_config(layout="wide")
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Movie Recommendation App")
st.markdown('#')


st.sidebar.markdown(f" ## :gear: Recommendation Settings")
st.sidebar.markdown('---')
no_of_rec = int(st.sidebar.slider("Select Number of Movie Recommendations", 1, 20, 10))
n_cols = st.sidebar.number_input("Select Number of columns", 2, 8, 5)
n_cols = int(n_cols)


@st.cache
def load_data():
    sim_matrix = pickle.load(open("cosine_sim.pkl", "rb"))
    return sim_matrix

cosine_sim = load_data()

movie = st.text_input("Enter your favorite movie:")
# st.button("Recommend!")


if movie != '':
    try:
        # movie_index = get_index_from_title(movie)
        # similar_movies = list(enumerate(cosine_sim[movie_index]))
        # sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
        res = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie}').json()
        id = res['results'][0]['id']
        poster = res['results'][0]['poster_path']
        col1, col2 = st.columns(2)
        col1.image(f'https://image.tmdb.org/t/p/w500{poster}', width=300)
        st.markdown('#')
        st.markdown(f"### :tada: Top {no_of_rec} Recommendations for {movie} :tada:")
        st.markdown('---')

        # top_movies = [get_title_from_index(sorted_similar_movies[i][0]) for i in range(10)]
        response = requests.get(f'https://api.themoviedb.org/3/movie/{id}/recommendations?api_key={api_key}&language=en-US&page=1').json()
        top_movies = [(response['results'][i]['original_title'], response['results'][i]['vote_average'])  for i in range(no_of_rec)]
        sorted_movies = sorted(top_movies, key=lambda x:x[1],reverse=True)
        top_sorted_movies = [x[0] for x in sorted_movies]

        posters = []
        titles = []
        for idx, movie in enumerate(top_sorted_movies):
            res = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie}').json()
            movie_posters = res['results'][0]['poster_path']
            movie_title = res['results'][0]['original_title']
            posters.append(f'https://image.tmdb.org/t/p/w500{movie_posters}')
            titles.append(movie_title)
         
        n_rows = int(1 + no_of_rec // n_cols)
        rows = [st.columns(n_cols) for _ in range(n_cols)]
        cols = [column for row in rows for column in row]
        for col, poster, title in zip(cols, posters, titles):
            col.markdown(f'###### {title}')
            col.image(poster, use_column_width=True)
          
    except:
        st.markdown(f"### :warning: Movie not found in database! :warning:")
else:
    pass


