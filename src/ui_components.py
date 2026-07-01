from math import exp
import streamlit as st

def render_movie_card(movie, trailer=None, section="general", row_idx=0, col_idx=0):
    poster = movie.get("poster", "")
    title = movie.get("title", "Unknown Title")

    movie_id = movie.get("id") or f"noid_{section}_{row_idx}_{col_idx}"
    details_key = f"details_{section}_{movie_id}_{row_idx}_{col_idx}"
    watch_key = f"watch_{section}_{movie_id}_{row_idx}_{col_idx}"
    trailer_key = f"trailer_{section}_{movie_id}_{row_idx}_{col_idx}"

    #CARD HTML
    st.markdown(
        f"""
        <div class="movie-card-container">
            <div class="movie-card">
                <img src="{poster}" alt="{title}" />
                <div class="caption">{title}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    # DETAILS BUTTON
    with col2:
        if st.button("ℹ️ Details", key=details_key, use_container_width=True):
            st.session_state.sidebar_movie = movie

    # WATCHLIST BUTTON
    with col2:
        if st.button("❤️ Add to Watchlist", key=watch_key, use_container_width=True):
            if movie not in st.session_state.watchlist:
                st.session_state.watchlist.append(movie)
                st.success(f"{title} added to Watchlist!")
            else:
                st.warning("Already in Watchlist")

    # TRAILER
    if trailer:
        with st.expander("▶️ Trailer", expanded=False):
            st.video(trailer, start_time=0)