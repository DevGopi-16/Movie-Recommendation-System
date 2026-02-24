import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# =========================================================
# 🌙 THEME TOGGLE SYSTEM
# =========================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Movie": ["Inception", "Interstellar", "The Dark Knight"],
        "Favorites": [10, 7, 12]
    })

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

theme = st.session_state.theme
df = st.session_state.df

# =========================================================
# 🎨 DYNAMIC COLORS
# =========================================================

if theme == "dark":
    bg_gradient = "linear-gradient(145deg, #0f172a, #1e293b)"
    text_color = "white"
    glass_bg = "rgba(255,255,255,0.08)"
else:
    bg_gradient = "linear-gradient(145deg, #f8fafc, #e2e8f0)"
    text_color = "#111"
    glass_bg = "rgba(255,255,255,0.55)"

# =========================================================
# 💎 PREMIUM GLASSMORPHISM CSS
# =========================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    transition: all 0.4s ease;
}}

.stApp {{
    background: {bg_gradient};
    color: {text_color};
    transition: 0.5s ease;
}}

/* ===== PREMIUM GLASS EFFECT ===== */

.glass {{
    background: {glass_bg};
    backdrop-filter: blur(25px) saturate(180%);
    -webkit-backdrop-filter: blur(25px) saturate(180%);
    
    border-radius: 28px;
    padding: 30px;

    border: 1px solid rgba(255, 255, 255, 0.25);

    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.35);

    transition: all 0.4s ease;
}}

.glass:hover {{
    transform: translateY(-6px);
    box-shadow:
        0 12px 40px rgba(0, 0, 0, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.45);
}}

.section-title {{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}}

.counter {{
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg,#00f5ff,#ff00c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.stButton>button {{
    border-radius: 30px;
    font-weight: 600;
    padding: 10px 20px;
    background: linear-gradient(45deg,#00f5ff,#ff00c8);
    color: white;
    border: none;
    transition: 0.3s;
}}

.stButton>button:hover {{
    transform: scale(1.05);
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🌌 PARTICLES BACKGROUND
# =========================================================

components.html("""
<div id="particles-js"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  particles: {
    number: { value: 40 },
    size: { value: 3 },
    color: { value: "#00f5ff" },
    line_linked: { enable: true, color: "#888" },
    move: { speed: 1.2 }
  }
});
</script>
""", height=0)

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([6,1])

with col1:
    st.markdown("<h1>🎬 Movie Dashboard</h1>", unsafe_allow_html=True)

with col2:
    if st.button("🌙 Toggle Theme"):
        toggle_theme()

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# CSV UPLOAD
# =========================================================

uploaded_file = st.file_uploader("Upload Movie CSV (Movie, Favorites)", type=["csv"])

if uploaded_file:
    st.session_state.df = pd.read_csv(uploaded_file)
    df = st.session_state.df

# =========================================================
# SEARCH & SORT
# =========================================================

search = st.text_input("Search Movie")
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[filtered_df["Movie"].str.contains(search, case=False)]

sort_option = st.selectbox("Sort Movies By Favorites",
                           ["Highest to Lowest", "Lowest to Highest"])

if sort_option == "Highest to Lowest":
    filtered_df = filtered_df.sort_values(by="Favorites", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="Favorites", ascending=True)

# =========================================================
# COUNTERS
# =========================================================

total_movies = len(filtered_df)
total_favorites = filtered_df["Favorites"].sum()
top_favorites = filtered_df["Favorites"].max() if not filtered_df.empty else 0

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f'<div class="glass"><div class="section-title">Total Movies</div><div class="counter">{total_movies}</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="glass"><div class="section-title">Total Favorites</div><div class="counter">{total_favorites}</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="glass"><div class="section-title">Top Favorites</div><div class="counter">{top_favorites}</div></div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

chart_font_color = "white" if theme == "dark" else "#111"

# =========================================================
# MAIN CHARTS
# =========================================================

colA, colB = st.columns(2)

with colA:
    st.markdown('<div class="glass"><div class="section-title">Top Favorite Movies</div>', unsafe_allow_html=True)
    fig_bar = px.bar(filtered_df, x="Movie", y="Favorites", text_auto=True)
    fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                          paper_bgcolor="rgba(0,0,0,0)",
                          font_color=chart_font_color,
                          height=350)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="glass"><div class="section-title">Favorites Distribution</div>', unsafe_allow_html=True)
    fig_donut = px.pie(filtered_df, names="Movie", values="Favorites", hole=0.6)
    fig_donut.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font_color=chart_font_color,
                            height=350)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ADVANCED ANALYTICS
# =========================================================

st.markdown("<br><br>", unsafe_allow_html=True)

# Monthly Trend
fig_month = go.Figure()
fig_month.add_trace(go.Scatter(
    x=["Jan","Feb","Mar","Apr"],
    y=[5,9,7,12],
    mode="lines+markers",
    line=dict(width=3),
    marker=dict(size=8)
))
fig_month.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font_color=chart_font_color,
                        height=320)

# Top 5 Ranking
top5 = filtered_df.sort_values(by="Favorites", ascending=False).head(5)
fig_rank = px.bar(top5, x="Favorites", y="Movie", orientation="h", text_auto=True)
fig_rank.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)",
                       font_color=chart_font_color,
                       height=320)

# Cumulative Growth
cumulative = filtered_df["Favorites"].cumsum()
fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(
    x=filtered_df["Movie"],
    y=cumulative,
    mode="lines+markers",
    line=dict(width=3),
    marker=dict(size=8)
))
fig_cum.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      font_color=chart_font_color,
                      height=320)

# Layout
colX, colY = st.columns(2)

with colX:
    st.markdown('<div class="glass"><div class="section-title">Monthly Favorites Trend</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_month, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with colY:
    st.markdown('<div class="glass"><div class="section-title">Top 5 Movies Ranking</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_rank, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="glass"><div class="section-title">Cumulative Favorites Growth</div>', unsafe_allow_html=True)
st.plotly_chart(fig_cum, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)