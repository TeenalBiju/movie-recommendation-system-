import streamlit as st
import pickle

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie = movie.lower()
    matching = movies[movies['title'].str.lower() == movie]
    if matching.empty:
        return []
    idx = matching.index[0]
    distances = similarity[idx]
    top5 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in top5]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #0f1117 !important;
    color: #ffffff;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.main-wrapper {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
}

.page-title {
    font-size: 48px;
    font-weight: 800;
    color: #ffffff;
    text-align: center;
    letter-spacing: -1px;
    margin-bottom: 8px;
}
.page-title span { color: #e50914; }

.page-subtitle {
    font-size: 16px;
    color: #666;
    text-align: center;
    margin-bottom: 48px;
    font-weight: 400;
}

.search-container {
    width: 100%;
    max-width: 560px;
    margin: 0 auto;
}

div[data-baseweb="select"] {
    width: 100% !important;
}
div[data-baseweb="select"] > div {
    background-color: #1e2130 !important;
    border: 1.5px solid #2e3250 !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    min-height: 54px !important;
    padding: 8px 16px !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #e50914 !important;
}
div[data-baseweb="select"] > div > div {
    color: #ffffff !important;
}
div[data-baseweb="select"] svg { fill: #666 !important; }

div[data-baseweb="popover"] > div {
    background-color: #1e2130 !important;
    border: 1px solid #2e3250 !important;
    border-radius: 12px !important;
}
li[role="option"] {
    color: #ccc !important;
    background-color: #1e2130 !important;
    font-size: 15px !important;
}
li[role="option"]:hover {
    background-color: #2a2f45 !important;
    color: #fff !important;
}
li[aria-selected="true"] {
    background-color: #e50914 !important;
    color: #fff !important;
}

label[data-testid="stWidgetLabel"] { display: none !important; }

.stButton { margin-top: 16px; }
.stButton > button {
    width: 260px !important;
    background-color: #e50914 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 30px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    transition: background 0.2s ease, transform 0.1s ease !important;
}
.stButton > button:hover {
    background-color: #b20710 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: scale(0.98) !important;
}

.results-title {
    font-size: 13px;
    font-weight: 600;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    text-align: center;
    margin: 48px 0 20px;
}

.rec-card {
    display: flex;
    align-items: center;
    gap: 18px;
    background: #1e2130;
    border: 1px solid #2a2f45;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 10px;
    transition: border-color 0.2s, transform 0.2s;
}
.rec-card:hover {
    border-color: #e50914;
    transform: translateX(6px);
}
.rec-num {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    min-width: 42px;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.rec-icon {
    width: 46px;
    height: 46px;
    background: #12141d;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.rec-info { flex: 1; }
.rec-title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    line-height: 1.3;
}
.rec-label {
    font-size: 12px;
    color: #555;
    margin-top: 4px;
}
.rec-arrow {
    font-size: 20px;
    color: #2a2f45;
}
.rec-card:hover .rec-arrow { color: #e50914; }

.error-box {
    background: #2a1215;
    border: 1px solid #5a1a1a;
    border-radius: 12px;
    padding: 16px 20px;
    color: #ff6b6b;
    font-size: 14px;
    font-weight: 500;
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-title">🎬 Movie <span>Recommender</span></div>
    <div class="page-subtitle">Select a movie and discover what to watch next</div>
    """, unsafe_allow_html=True)

    selected_movie = st.selectbox(
        "movie",
        movies['title'].values,
        label_visibility="collapsed"
    )

    clicked = st.button("Get Recommendations")

    if clicked:
        results = recommend(selected_movie)
        if not results:
            st.markdown('<div class="error-box">Movie not found. Please try another title.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="results-title">Recommended for you</div>', unsafe_allow_html=True)
            icons = ["🎬", "🎭", "🌟", "🎞️", "🍿"]
            for i, title in enumerate(results, 1):
                st.markdown(f"""
                <div class="rec-card">
                    <div class="rec-num">0{i}</div>
                    <div class="rec-icon">{icons[i-1]}</div>
                    <div class="rec-info">
                        <div class="rec-title">{title}</div>
                        <div class="rec-label">Similar to {selected_movie}</div>
                    </div>
                    <div class="rec-arrow">→</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)