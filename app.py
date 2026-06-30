import streamlit as st
import pandas as pd
import os
import requests
import tmdbsimple as tmdb
import concurrent.futures
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import ast

from src.styles import load_css
from src.ui_components import render_movie_card
from src.preprocess import preprocess_data
from src.recommender import MovieRecommender
from src.cache import cached_call
from src.tmdb_api import (
    get_trailer,
    get_movie_id_by_title,
    get_trending_movies,
    fetch_category_movies,
    get_movie_details
)

st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

#TMDB CONFIG 
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
tmdb.API_KEY = TMDB_API_KEY


if not TMDB_API_KEY:
    st.error("TMDB API key not found. Set TMDB_API_KEY environment variable.")
    st.stop()

    
MOVIES_PER_PAGE = 15


#SESSION STATE 
if "category_page" not in st.session_state:
    st.session_state.category_page = 1
if "last_category" not in st.session_state:
    st.session_state.last_category = None

# Add recommendation and sidebar state
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
if "sidebar_movie_id" not in st.session_state:
    st.session_state.sidebar_movie_id = None

# WATCHLIST STATE
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

#HEADER
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)


#LOAD + PREPROCESS DATA 
@st.cache_data(show_spinner="📦 Loading movie dataset...")
def load_and_process_movies():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    movies_file = os.path.join(BASE_DIR, "Data", "tmdb_5000_movies.csv")
    credits_file = os.path.join(BASE_DIR, "Data", "tmdb_5000_credits.csv")

    movies = pd.read_csv(movies_file)
    credits = pd.read_csv(credits_file)

    merged = movies.merge(credits, on="title")
    return preprocess_data(merged)

processed_movies = load_and_process_movies()
movie_list = processed_movies["title"].values

#LOAD RECOMMENDER 
@st.cache_resource(show_spinner="Building recommendation model...")
def load_recommender(df):
    return MovieRecommender(df)

recommender = load_recommender(processed_movies)

#TRENDING MOVIES
st.markdown("## 🔥 Trending Now")
trending_movies = get_trending_movies(TMDB_API_KEY)
num_cols = 5

def fetch_trailer(movie):
    movie_id = movie.get("id") or get_movie_id_by_title(movie.get("title",""), TMDB_API_KEY)
    return get_trailer(movie_id, TMDB_API_KEY) if movie_id else None

with concurrent.futures.ThreadPoolExecutor() as executor:
    trending_trailers = list(executor.map(fetch_trailer, trending_movies))

for row_i in range(0, len(trending_movies), num_cols):
    cols = st.columns(num_cols)
    for col_j, (col, movie, trailer) in enumerate(
        zip(cols, trending_movies[row_i:row_i+num_cols], trending_trailers[row_i:row_i+num_cols])
    ):
        with col:
            render_movie_card(movie, trailer, section="trending", row_idx=row_i, col_idx=col_j)

#SEARCH & RECOMMENDATIONS
st.markdown("## 🔍 Find a Movie")

selected_movie = st.selectbox(
    "",
    movie_list,
    index=list(movie_list).index("Avatar") if "Avatar" in movie_list else 0,
    label_visibility="collapsed"
)

if st.button("🎯 Recommend", use_container_width=True):
    with st.spinner("Finding similar movies..."):
        st.session_state.recommendations = recommender.recommend(selected_movie, TMDB_API_KEY)

# Display recommendations from session_state
if st.session_state.recommendations:
    st.markdown("## 🍿 Recommended Movies")
    num_cols = 5

    def fetch_trailer_recommend(movie):
        movie_id = movie.get("id") or get_movie_id_by_title(movie.get("title",""), TMDB_API_KEY)
        return get_trailer(movie_id, TMDB_API_KEY) if movie_id else None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        trailers = list(executor.map(fetch_trailer_recommend, st.session_state.recommendations))

    for row_i in range(0, len(st.session_state.recommendations), num_cols):
        cols = st.columns(num_cols)
        for col_j, (col, movie, trailer) in enumerate(
            zip(cols, st.session_state.recommendations[row_i:row_i+num_cols], trailers[row_i:row_i+num_cols])
        ):
            with col:
                render_movie_card(movie, trailer, section="recommend", row_idx=row_i, col_idx=col_j)

# CATEGORY SECTION 
st.markdown("## 🎞 Browse by Category")

category = st.selectbox(
    "",
    ["Hollywood", "Bollywood", "K-Drama", "Action", "Comedy", "Romance", "Horror",
     "Thriller", "Sci-Fi", "Animation", "Drama", "Crime", "Fantasy", "Adventure",
     "Family", "Mystery", "War", "Music", "Western"],
    index=None,
    placeholder="Choose category"
)

if category != st.session_state.last_category:
    st.session_state.category_page = 1
    st.session_state.last_category = category

raw_movies = cached_call(
    fetch_category_movies,
    TMDB_API_KEY,
    category,
    st.session_state.category_page
)

movies = [m for m in raw_movies if m.get("id") and m.get("title")]

num_cols = 5

def fetch_trailer_category(movie):
    movie_id = movie.get("id")
    return get_trailer(movie_id, TMDB_API_KEY) if movie_id else None

with concurrent.futures.ThreadPoolExecutor() as executor:
    trailers = list(executor.map(fetch_trailer_category, movies))

for row_i in range(0, len(movies), num_cols):
    cols = st.columns(num_cols)
    for col_j, (col, movie, trailer) in enumerate(
        zip(cols, movies[row_i:row_i+num_cols], trailers[row_i:row_i+num_cols])
    ):
        with col:
            render_movie_card(movie, trailer, section="category", row_idx=row_i, col_idx=col_j)

#CATEGORY PAGINATION 
col1, _, col3 = st.columns([1,2,1])
with col1:
    if st.button("⬅ Previous", disabled=st.session_state.category_page == 1):
        st.session_state.category_page -= 1
        st.rerun()

with col3:
    if st.button("Next ➡"):
        st.session_state.category_page += 1
        st.rerun()

# MOUSE-RESPONSIVE 3D TILT 
components.html("""
<script>
document.querySelectorAll('.movie-card-container').forEach(container => {
    const card = container.querySelector('.movie-card');
    container.addEventListener('mousemove', e => {
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const cx = rect.width/2;
        const cy = rect.height/2;
        const dx = (x - cx) / cx;
        const dy = (y - cy) / cy;
        const rotateX = dy * 8;
        const rotateY = dx * 8;
        card.style.transform = `rotateX(${ -rotateX }deg) rotateY(${ rotateY }deg) scale(1.08)`;
    });
    container.addEventListener('mouseleave', e => {
        card.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1.0)';
    });
});
</script>
""", height=0)



# WATCHLIST SECTION

if st.session_state.watchlist:
    st.markdown("## ❤️ Your Watchlist")

    num_cols = 5
    watchlist = st.session_state.watchlist

    for row_i in range(0, len(watchlist), num_cols):
        cols = st.columns(num_cols)

        for col_j, (col, movie) in enumerate(
            zip(cols, watchlist[row_i:row_i+num_cols])
        ):
            with col:
                if movie.get("poster_path"):
                    st.image(
                        f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
                    )
                st.caption(movie.get("title"))

                # Remove button
                if st.button(
                    "❌ Remove",
                    key=f"remove_{row_i}_{col_j}_{movie.get('id')}"
                ):
                    st.session_state.watchlist.remove(movie)
                    st.rerun()



# SAVE WATCHLIST TO CSV
if st.session_state.watchlist:

    st.markdown("### 💾 Save Your Watchlist")

    if st.button("Download Watchlist as CSV", use_container_width=True):

        # Convert to DataFrame safely
        df = pd.DataFrame(st.session_state.watchlist)

        # Detect rating column safely
        rating_column = None
        for col in ["vote_average", "rating", "score"]:
            if col in df.columns:
                rating_column = col
                break

        # Keep only useful columns
        columns_to_keep = ["id", "title", "release_date"]
        if rating_column:
            columns_to_keep.append(rating_column)

        df = df[[col for col in columns_to_keep if col in df.columns]]

        file_path = "watchlist.csv"
        df.to_csv(file_path, index=False)

        st.success("✅ Watchlist saved successfully!")

        # Direct download button (cleaner way — no file open needed)
        st.download_button(
            label="📥 Download CSV File",
            data=df.to_csv(index=False),
            file_name="watchlist.csv",
            mime="text/csv"
        )
                  
#SIDEBAR DETAILS 
if "sidebar_movie" in st.session_state and st.session_state.sidebar_movie:
    movie = st.session_state.sidebar_movie
    details = get_movie_details(movie.get("id"), TMDB_API_KEY)
    if details:
        st.sidebar.markdown(f"## 🎬 {details.get('title')}")
        if details.get("poster_path"):
            st.sidebar.image(f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}", width=300)
        st.sidebar.markdown(f"**Release Date:** {details.get('release_date', 'N/A')}")
        st.sidebar.markdown(f"**Rating:** {details.get('vote_average', 'N/A')} / 10")
        genres = ', '.join([g['name'] for g in details.get('genres', [])])
        st.sidebar.markdown(f"**Genres:** {genres if genres else 'N/A'}")
        st.sidebar.markdown(f"**Overview:** {details.get('overview', 'No overview available.')}")
        trailer_url = get_trailer(movie.get('id'), TMDB_API_KEY)
        if trailer_url:
            st.sidebar.video(trailer_url, start_time=0)

