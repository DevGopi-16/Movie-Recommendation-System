import streamlit as st

def load_css():
    st.markdown("""
<style>

/* ===========================
   GOOGLE FONT
=========================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');


/* ===========================
   GLOBAL
=========================== */

html,
body,
[class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{

background:
radial-gradient(circle at top left,#4f46e5 0%,transparent 28%),
radial-gradient(circle at bottom right,#2563eb 0%,transparent 25%),
linear-gradient(
135deg,
#0f172a,
#111827,
#020617
);

background-attachment:fixed;
color:white;
}


/* Hide Streamlit Menu */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
background:transparent;
}


/* ===========================
   SCROLLBAR
=========================== */

::-webkit-scrollbar{
width:10px;
}

::-webkit-scrollbar-track{
background:transparent;
}

::-webkit-scrollbar-thumb{

background:rgba(255,255,255,.2);

border-radius:20px;

}

::-webkit-scrollbar-thumb:hover{

background:rgba(255,255,255,.4);

}


/* ===========================
   GLASS CARD
=========================== */

.glass{

background:rgba(255,255,255,.08);

backdrop-filter:blur(24px);

-webkit-backdrop-filter:blur(24px);

border:1px solid rgba(255,255,255,.12);

border-radius:30px;

padding:24px;

box-shadow:

0 8px 40px rgba(0,0,0,.35);

}


/* ===========================
   GLASS BUTTON
=========================== */

.stButton>button{

width:100%;

height:52px;

background:rgba(255,255,255,.12);

color:white;

border:none;

border-radius:16px;

backdrop-filter:blur(20px);

transition:.35s;

font-weight:600;

}

.stButton>button:hover{

transform:translateY(-4px);

background:rgba(255,255,255,.2);

box-shadow:

0 15px 35px rgba(79,70,229,.45);

}


/* ===========================
   INPUT
=========================== */

.stSelectbox div[data-baseweb="select"]{

background:rgba(255,255,255,.08);

border-radius:18px;

backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.12);

}


/* ===========================
   TEXT INPUT
=========================== */

.stTextInput input{

background:rgba(255,255,255,.08);

color:white;

border-radius:18px;

border:1px solid rgba(255,255,255,.12);

}


/* ===========================
   SIDEBAR
=========================== */

[data-testid="stSidebar"]{

background:

rgba(255,255,255,.06);

backdrop-filter:blur(30px);

border-right:

1px solid rgba(255,255,255,.1);

}


/* ===========================
   HEADINGS
=========================== */

h1{

font-size:46px;

font-weight:700;

}

h2{

font-size:34px;

font-weight:700;

margin-top:20px;

}

h3{

font-size:24px;

}


/* ===========================
   IMAGE
=========================== */

img{

border-radius:20px;

transition:.4s;

}

img:hover{

transform:scale(1.03);

}


/* ===========================
   ANIMATION
=========================== */

@keyframes fadeUp{

0%{

opacity:0;

transform:translateY(30px);

}

100%{

opacity:1;

transform:translateY(0);

}

}

.fade{

animation:fadeUp .7s ease;

}


/* ===========================
   EXPANDER
=========================== */

.streamlit-expanderHeader{

background:rgba(255,255,255,.05);

}


/* ===========================
   METRIC
=========================== */

[data-testid="metric-container"]{

background:rgba(255,255,255,.06);

border-radius:20px;

padding:18px;

}


/* ===========================
   HORIZONTAL LINE
=========================== */

hr{

border:none;

height:1px;

background:rgba(255,255,255,.08);

margin:25px 0;

}

</style>
""", unsafe_allow_html=True)