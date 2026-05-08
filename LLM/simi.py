import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
from pypdf import PdfReader
import speech_recognition as sr
import numpy as np
import re
import math
import collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
from rapidfuzz import process as fuzz_process

# ── FIX 6: Use environment variable instead of hardcoded API key ───────────────
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "your-gemini-api-key-here"))

# ── FIX 4: Only ONE st.set_page_config call, at the very top ─────────────────
st.set_page_config(page_title="Ultra AI", page_icon="🤖", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username.strip() == "admin" and password.strip() == "password":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

st.sidebar.title("Controls")
mode = st.sidebar.selectbox("Select Mode", ["Chatbot", "PDF chat", "product"])

temperature = st.sidebar.slider("Creativity", 0.0, 1.0, 0.7)
style = st.sidebar.selectbox("Response Style", ["Simple", "Detailed", "Professional"])

system_prompt = f"You are a helpful assistant. Explain things in a {style} way in English."

# ── FIX 1: Use a valid Gemini model name ─────────────────────────────────────
model = genai.GenerativeModel(model_name="gemini-3.1-flash-lite-preview       ", system_instruction=system_prompt)


def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except Exception as e:
        st.error(f"Error recognizing speech: {e}")
        return None


if mode == "Chatbot":
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    st.title("Pro Gemini Chatbot")

    # ── FIX 5: Display history loop is separate from the input widgets ────────
    for message in st.session_state.chat.history:
        role = "You" if message.role == "user" else "AI"
        st.write(f"**{role}:** {message.parts[0].text}")

    # Input widgets outside the history loop
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.chat_input("Type your question")
    with col2:
        if st.button("🎤 Speak"):
            voice_result = get_voice_input()
            if voice_result:
                # ── FIX 3: f-string with f prefix ────────────────────────────
                st.write(f"**You asked:** {voice_result}")
                # Send voice input to chat
                response = st.session_state.chat.send_message(
                    voice_result,
                    # ── FIX 2: Correct dict key as string "temperature" ───────
                    generation_config={"temperature": temperature}
                )
                st.write(f"**AI:** {response.text}")
                st.rerun()

    if user_input:
        # ── FIX 2: Correct generation_config key ─────────────────────────────
        response = st.session_state.chat.send_message(
            user_input,
            generation_config={"temperature": temperature}
        )
        st.write(f"**You:** {user_input}")
        st.write(f"**AI:** {response.text}")

elif mode == "PDF chat":
    st.title("PDF Chat")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        questions = st.text_input("Enter questions about the PDF, separated by commas")

        if questions:
            prompt = f"Answer from the pdf\n{text}\nQuestions: {questions}"
            response = model.generate_content(prompt, generation_config={"temperature": temperature})
            st.write(f"**AI:** {response.text}")

elif mode == "product":
    # ── FIX 4: No second st.set_page_config here ─────────────────────────────

    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

    .search-hero {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0d1b2a 100%);
        border-radius: 20px; padding: 2.5rem 2.5rem 2rem;
        margin-bottom: 2rem; border: 1px solid rgba(99,102,241,0.3);
    }
    .hero-title { font-size: 2rem; font-weight: 600; color: #fff; margin-bottom: 0.2rem; letter-spacing: -0.5px; }
    .hero-sub { font-size: 0.95rem; color: rgba(255,255,255,0.5); margin-bottom: 1.5rem; }
    .hero-stats { display: flex; gap: 2rem; }
    .hero-stat { color: rgba(255,255,255,0.55); font-size: 0.8rem; }
    .hero-stat span { color: #a5b4fc; font-weight: 600; font-size: 0.95rem; }

    .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px,1fr)); gap: 1rem; margin-top: 1rem; }
    .product-card {
        background: #fff; border: 1px solid #e8e8f0; border-radius: 14px;
        overflow: hidden; transition: box-shadow .2s, transform .2s; position: relative;
    }
    .product-card:hover { box-shadow: 0 8px 30px rgba(99,102,241,0.13); transform: translateY(-2px); }
    .card-img { width: 100%; height: 160px; object-fit: cover; background: #f3f4f6; display: block; }
    .card-body { padding: 0.9rem 1rem 1rem; }
    .card-category {
        font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.06em; padding: 2px 7px; border-radius: 20px; display: inline-block; margin-bottom: 0.4rem;
    }
    .cat-Electronics { background:#ede9fe; color:#5b21b6; }
    .cat-Clothing     { background:#fce7f3; color:#9d174d; }
    .cat-Footwear     { background:#fef3c7; color:#92400e; }
    .cat-Furniture    { background:#d1fae5; color:#065f46; }
    .cat-Home         { background:#dbeafe; color:#1e40af; }
    .product-name { font-size: 0.9rem; font-weight: 600; color: #111827; margin-bottom: 0.5rem; line-height: 1.35; }
    .card-row { display: flex; justify-content: space-between; align-items: center; margin-top: 0.4rem; }
    .product-price { font-size: 1rem; font-weight: 600; color: #111827; font-family: 'DM Mono', monospace; }
    .pred-price { font-size: 0.72rem; color: #6b7280; margin-top: 2px; }
    .cluster-badge {
        font-size: 0.68rem; padding: 2px 6px; border-radius: 20px;
        background: #f3f4f6; color: #6b7280; font-weight: 500;
    }
    .match-label { font-size: 0.68rem; color: #9ca3af; display: flex; justify-content: space-between; margin-top: 6px; margin-bottom: 2px; }
    .match-bar-bg { height: 4px; background: #f3f4f6; border-radius: 99px; overflow: hidden; }
    .match-bar-fill { height: 100%; border-radius: 99px; }
    .score-breakdown { display: flex; gap: 6px; margin-top: 6px; }
    .score-pill { font-size: 0.65rem; padding: 2px 6px; border-radius: 99px; font-weight: 500; }
    .score-tfidf    { background: #ede9fe; color: #5b21b6; }
    .score-semantic { background: #d1fae5; color: #065f46; }
    .rank-badge {
        position: absolute; top: 8px; right: 8px; width: 22px; height: 22px;
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 0.68rem; font-weight: 600; z-index: 2;
    }
    .rank-1 { background: #fef3c7; color: #92400e; }
    .rank-2 { background: #e5e7eb; color: #374151; }
    .rank-3 { background: #fce7f3; color: #9d174d; }
    .rank-n { background: rgba(0,0,0,0.45); color: #fff; }
    .explain-box {
        background: #f8f9ff; border: 1px solid #e0e0f0; border-radius: 10px;
        padding: 0.7rem 1rem; margin-top: 0.5rem; font-size: 0.78rem;
    }
    .explain-title { font-weight: 600; color: #374151; margin-bottom: 4px; font-size: 0.8rem; }
    .explain-term { display: inline-block; background: #ede9fe; color: #5b21b6; border-radius: 6px; padding: 2px 7px; margin: 2px 2px 2px 0; font-size: 0.72rem; }
    .nl-tag { background: #dbeafe; color: #1e40af; border-radius: 6px; padding: 2px 8px; font-size: 0.75rem; display: inline-block; margin: 2px; font-weight: 500; }
    .result-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem; padding-bottom: 0.6rem; border-bottom: 1px solid #f0f0f5; }
    .result-count { font-size: 0.85rem; color: #6b7280; }
    .result-count strong { color: #111827; }
    .no-results { text-align: center; padding: 4rem 2rem; color: #9ca3af; }
    .no-results-title { font-size: 1rem; font-weight: 600; color: #374151; margin-bottom: 0.4rem; }
    .disc-badge{position:absolute;top:8px;left:8px;background:#e53935;color:#fff;font-size:.65rem;font-weight:700;padding:2px 6px;border-radius:4px;z-index:2;}
    .card-brand{font-size:.72rem;color:#6b7280;margin-bottom:2px;font-weight:500;}
    .card-rating{display:flex;align-items:center;gap:4px;margin-bottom:4px;}
    .stars{color:#f59e0b;font-size:.78rem;letter-spacing:1px;}
    .rating-num{font-size:.72rem;color:#6b7280;font-weight:500;}
    .similar-header { font-size: 0.8rem; font-weight: 600; color: #374151; margin: 1.2rem 0 0.5rem; }
    .similar-chip {
        display: inline-block; background: #f3f4f6; border: 1px solid #e5e7eb;
        border-radius: 8px; padding: 4px 10px; margin: 3px; font-size: 0.78rem; color: #374151; cursor: pointer;
    }
    .analytics-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.5rem; }
    .analytics-card { background: #fff; border: 1px solid #e8e8f0; border-radius: 14px; padding: 1.1rem 1.3rem; }
    .analytics-label { font-size: 0.75rem; color: #6b7280; margin-bottom: 0.25rem; }
    .analytics-value { font-size: 1.5rem; font-weight: 600; color: #111827; font-family: 'DM Mono', monospace; }
    .insight-row { display: flex; align-items: center; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid #f3f4f6; font-size: 0.85rem; }
    .insight-row:last-child { border-bottom: none; }
    .insight-key { color: #374151; font-weight: 500; }
    .insight-val { color: #6366f1; font-weight: 600; font-family: 'DM Mono', monospace; }
    .ab-col { background: #fff; border: 1px solid #e8e8f0; border-radius: 12px; padding: 1rem; }
    .ab-title { font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; color: #9ca3af; margin-bottom: 0.7rem; }
    .ab-metric { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; font-size: 0.83rem; border-bottom: 1px solid #f3f4f6; }
    .ab-metric:last-child { border: none; }
    .ab-win { color: #059669; font-weight: 600; }
    .trend-item { display: flex; align-items: center; gap: 8px; padding: 5px 0; font-size: 0.85rem; border-bottom: 1px solid #f3f4f6; }
    .trend-item:last-child { border: none; }
    .trend-count { font-family: 'DM Mono', monospace; color: #6366f1; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # MODEL LOADING (all cached)
    # ══════════════════════════════════════════════════════════════════════════
    @st.cache_resource
    def load_all():
        # FIX: correct filename with space (not underscore)
        import os
        # Try both possible filenames
        csv_path = "real product2.csv"
        if not os.path.exists(csv_path):
            csv_path = "real_product2.csv"
        if not os.path.exists(csv_path):
            st.error(f"CSV file not found. Please make sure 'real product2.csv' is in the same folder as app.py")
            st.stop()
        df = pd.read_csv(csv_path)
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        if "category" not in df.columns:
            df["category"] = "Other"
        df["category"] = df["category"].fillna("Other")

        if "price" not in df.columns and "discounted_price" in df.columns:
            df["price"] = df["discounted_price"]
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)

        if "product_name" not in df.columns:
            df["product_name"] = "Unknown Product"
        df["product_name"] = df["product_name"].fillna("Unknown Product")

        if "brand" not in df.columns:
            df["brand"] = df["product_name"].str.split().str[0]
        df["brand"] = df["brand"].fillna("Unknown")

        if "description" not in df.columns:
            df["description"] = ""
        df["description"] = df["description"].fillna("")

        if "sub_category" not in df.columns:
            df["sub_category"] = df["category"]
        df["sub_category"] = df["sub_category"].fillna(df["category"])

        if "rating" not in df.columns:
            df["rating"] = np.nan
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

        if "retail_price" not in df.columns:
            df["retail_price"] = df["price"]
        df["retail_price"] = pd.to_numeric(df["retail_price"], errors="coerce").fillna(df["price"])

        # FIX 3: Try multiple possible image column names from the CSV
        image_col_candidates = ["image_url", "image", "img_url", "img", "photo", "photo_url",
                                  "thumbnail", "thumbnail_url", "product_image", "product_img"]
        found_img_col = None
        for candidate in image_col_candidates:
            if candidate in df.columns:
                found_img_col = candidate
                break
        if found_img_col and found_img_col != "image_url":
            df["image_url"] = df[found_img_col]
        elif "image_url" not in df.columns:
            df["image_url"] = ""
        df["image_url"] = df["image_url"].fillna("").astype(str).str.strip()

        df["search_text"] = (
            df["product_name"].str.lower() + " " +
            df["product_name"].str.lower() + " " +
            df["product_name"].str.lower() + " " +
            df["brand"].str.lower() + " " +
            df["category"].str.lower() + " " +
            df["sub_category"].str.lower() + " " +
            df["description"].str.lower().str[:100]
        )

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        tfidf_mat = vectorizer.fit_transform(df["search_text"])

        svd = TruncatedSVD(n_components=50, random_state=42)
        lsa_mat = svd.fit_transform(tfidf_mat)

        km = KMeans(n_clusters=8, random_state=42, n_init=10)
        df["cluster"] = km.fit_predict(lsa_mat)

        item_sim = cosine_similarity(lsa_mat)

        le_cat = LabelEncoder()
        le_brand = LabelEncoder()
        df["cat_enc"] = le_cat.fit_transform(df["category"])
        df["brand_enc"] = le_brand.fit_transform(df["brand"])
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(df[["cat_enc", "brand_enc"]], df["price"])
        df["predicted_price"] = rf.predict(df[["cat_enc", "brand_enc"]]).round(0).astype(int)

        df["rating_filled"] = df["rating"].fillna(
            df.groupby("category")["rating"].transform("median")
        ).fillna(3.0)
        df["popularity_score"] = df.groupby("category")["rating_filled"].transform(
            lambda x: (x - x.min()) / (x.max() - x.min() + 1)
        )

        return df, vectorizer, tfidf_mat, svd, lsa_mat, km, item_sim, rf, le_cat, le_brand

    df, vectorizer, tfidf_mat, svd, lsa_mat, km, item_sim, rf, le_cat, le_brand = load_all()
    CATEGORIES = ["All"] + sorted(df["category"].unique().tolist())
    PRICE_MIN = int(df["price"].min())
    PRICE_MAX = int(df["price"].max())
    FEAT_NAMES = vectorizer.get_feature_names_out()
    CLUSTER_NAMES = {
        0: "Budget picks", 1: "Electronics", 2: "Fashion",
        3: "Home & Living", 4: "Premium", 5: "Footwear",
        6: "Appliances", 7: "Luxury",
    }

    # ══════════════════════════════════════════════════════════════════════════
    # HELPER FUNCTIONS
    # ══════════════════════════════════════════════════════════════════════════

    def cat_css(cat):
        return {"Electronics": "cat-Electronics", "Clothing": "cat-Clothing",
                "Footwear": "cat-Footwear", "Furniture": "cat-Furniture",
                "Home Appliances": "cat-Home"}.get(cat, "cat-Home")

    def bar_color(score):
        if score >= 0.7: return "#10b981"
        if score >= 0.4: return "#6366f1"
        return "#f59e0b"

    import base64 as _b64mod

    def _b64(svg: str) -> str:
        return "data:image/svg+xml;base64," + _b64mod.b64encode(svg.encode()).decode()

    _PH  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f0f4ff"/><rect x="155" y="30" width="90" height="160" rx="18" fill="#1c1c1e"/><rect x="161" y="50" width="78" height="120" rx="4" fill="{s}"/><rect x="185" y="42" width="30" height="5" rx="2.5" fill="#3a3a3c"/><circle cx="200" cy="195" r="8" fill="#3a3a3c"/></svg>'
    _LT  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f5f5f5"/><rect x="80" y="70" width="240" height="155" rx="8" fill="{b}"/><rect x="88" y="78" width="224" height="135" rx="4" fill="{s}"/><rect x="60" y="225" width="280" height="15" rx="4" fill="#ccc"/><rect x="150" y="225" width="100" height="8" rx="2" fill="#aaa"/></svg>'
    _SK  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fff9f0"/><path d="M80 200 Q100 140 160 130 Q200 125 240 140 L310 155 Q340 160 330 185 Q320 200 280 200 Z" fill="{u}"/><path d="M80 200 L330 200 L325 215 Q300 225 200 225 Q120 225 90 215 Z" fill="{sl}"/><path d="M155 130 L155 200" stroke="{sl}" stroke-width="3"/><path d="M180 128 L180 200" stroke="{sl}" stroke-width="2.5"/><path d="M205 128 L205 200" stroke="{sl}" stroke-width="2.5"/><path d="M230 133 L230 200" stroke="{sl}" stroke-width="2.5"/></svg>'

    _PRODUCT_IMAGES = {
        "iPhone 13": _b64(_PH.replace("{s}", "#3a7bd5")),
        "iPhone 14": _b64(_PH.replace("{s}", "#5856d6")),
        "Samsung Galaxy S21": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f0f8ff"/><rect x="153" y="28" width="94" height="170" rx="16" fill="#1428a0"/><rect x="160" y="48" width="80" height="130" rx="4" fill="#4fc3f7"/><rect x="189" y="37" width="22" height="5" rx="2.5" fill="#0d1a6e"/><circle cx="200" cy="188" r="7" fill="#0d1a6e"/></svg>'),
        "Samsung Galaxy S22": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f0f8ff"/><rect x="153" y="28" width="94" height="170" rx="16" fill="#6200ea"/><rect x="160" y="48" width="80" height="130" rx="4" fill="#b39ddb"/><rect x="189" y="37" width="22" height="5" rx="2.5" fill="#4a00b0"/><circle cx="200" cy="188" r="7" fill="#4a00b0"/></svg>'),
        "OnePlus 11": _b64(_PH.replace("{s}", "#eb0029").replace("#1c1c1e", "#111")),
        "Realme Narzo": _b64(_PH.replace("{s}", "#ffd600").replace("#1c1c1e", "#222")),
        "Redmi Note 12": _b64(_PH.replace("{s}", "#ff6900").replace("#1c1c1e", "#111")),
        "Dell Inspiron Laptop": _b64(_LT.replace("{b}", "#2c5f9e").replace("{s}", "#a8d4ff")),
        "HP Pavilion Laptop": _b64(_LT.replace("{b}", "#0096d6").replace("{s}", "#b3d9f0")),
        "MacBook Air": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f9f9f9"/><rect x="75" y="65" width="250" height="160" rx="10" fill="#d4d4d2"/><rect x="83" y="73" width="234" height="140" rx="4" fill="#1d1d1f"/><circle cx="200" cy="72" r="3" fill="#555"/><rect x="50" y="225" width="300" height="14" rx="5" fill="#c0c0be"/><rect x="155" y="225" width="90" height="6" rx="3" fill="#aaa"/></svg>'),
        "Sony Headphones": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fff8f0"/><path d="M140 150 Q140 80 200 80 Q260 80 260 150" fill="none" stroke="#111" stroke-width="14" stroke-linecap="round"/><rect x="120" y="145" width="36" height="55" rx="14" fill="#222"/><rect x="244" y="145" width="36" height="55" rx="14" fill="#222"/><rect x="126" y="152" width="24" height="40" rx="10" fill="#555"/><rect x="250" y="152" width="24" height="40" rx="10" fill="#555"/></svg>'),
        "JBL Speaker": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fffde7"/><rect x="140" y="80" width="120" height="140" rx="30" fill="#f57f17"/><circle cx="200" cy="150" r="38" fill="#e65100"/><circle cx="200" cy="150" r="22" fill="#bf360c"/><circle cx="200" cy="150" r="8" fill="#111"/><circle cx="172" cy="105" r="7" fill="#ff8f00"/><circle cx="228" cy="105" r="7" fill="#ff8f00"/></svg>'),
        "Boat Earbuds": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f3e5f5"/><ellipse cx="160" cy="155" rx="28" ry="35" fill="#6a1b9a"/><ellipse cx="240" cy="155" rx="28" ry="35" fill="#6a1b9a"/><path d="M160 120 Q200 95 240 120" fill="none" stroke="#9c27b0" stroke-width="6" stroke-linecap="round"/><circle cx="160" cy="155" r="12" fill="#ab47bc"/><circle cx="240" cy="155" r="12" fill="#ab47bc"/></svg>'),
        "Samsung Washing Machine": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e8f5e9"/><rect x="120" y="50" width="160" height="190" rx="10" fill="#eceff1"/><rect x="128" y="58" width="144" height="174" rx="7" fill="#fff"/><circle cx="200" cy="165" r="55" fill="#b0bec5"/><circle cx="200" cy="165" r="44" fill="#e3f2fd"/><circle cx="200" cy="165" r="20" fill="#1565c0" opacity="0.4"/><rect x="135" y="68" width="60" height="12" rx="4" fill="#90a4ae"/><circle cx="215" cy="74" r="6" fill="#ef5350"/><circle cx="232" cy="74" r="6" fill="#66bb6a"/></svg>'),
        "Whirlpool AC": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e3f2fd"/><rect x="80" y="100" width="240" height="100" rx="12" fill="#eceff1"/><rect x="88" y="108" width="224" height="84" rx="8" fill="#fff"/><rect x="96" y="125" width="208" height="5" rx="2" fill="#b0bec5"/><rect x="96" y="138" width="208" height="5" rx="2" fill="#b0bec5"/><rect x="96" y="151" width="208" height="5" rx="2" fill="#b0bec5"/><rect x="96" y="164" width="208" height="5" rx="2" fill="#b0bec5"/><circle cx="285" cy="118" r="8" fill="#42a5f5"/><circle cx="270" cy="118" r="6" fill="#4caf50"/></svg>'),
        "LG Refrigerator": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e0f7fa"/><rect x="140" y="30" width="120" height="240" rx="10" fill="#eceff1"/><rect x="148" y="38" width="104" height="95" rx="6" fill="#b2dfdb"/><rect x="148" y="142" width="104" height="120" rx="6" fill="#e0f7fa"/><rect x="236" y="78" width="5" height="20" rx="2" fill="#78909c"/><rect x="236" y="188" width="5" height="20" rx="2" fill="#78909c"/><line x1="148" y1="140" x2="252" y2="140" stroke="#b0bec5" stroke-width="3"/></svg>'),
        "Prestige Cooker": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fff3e0"/><rect x="130" y="115" width="140" height="110" rx="12" fill="#c62828"/><ellipse cx="200" cy="115" rx="70" ry="18" fill="#e53935"/><rect x="186" y="78" width="28" height="40" rx="5" fill="#555"/><circle cx="200" cy="75" r="9" fill="#333"/><rect x="118" y="155" width="14" height="35" rx="5" fill="#b71c1c"/><rect x="268" y="155" width="14" height="35" rx="5" fill="#b71c1c"/></svg>'),
        "Philips Mixer Grinder": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fce4ec"/><rect x="165" y="185" width="70" height="20" rx="5" fill="#880e4f"/><ellipse cx="200" cy="185" rx="50" ry="12" fill="#ad1457"/><rect x="168" y="105" width="64" height="82" rx="8" fill="#e91e63"/><ellipse cx="200" cy="105" rx="32" ry="9" fill="#f06292"/><rect x="190" y="68" width="20" height="40" rx="5" fill="#555"/><circle cx="200" cy="65" r="8" fill="#333"/></svg>'),
        "Ikea Study Table": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fff8e1"/><rect x="70" y="130" width="260" height="18" rx="4" fill="#795548"/><rect x="80" y="148" width="16" height="90" rx="4" fill="#6d4c41"/><rect x="304" y="148" width="16" height="90" rx="4" fill="#6d4c41"/><rect x="80" y="210" width="240" height="14" rx="3" fill="#8d6e63"/><rect x="100" y="82" width="180" height="52" rx="4" fill="#a1887f" opacity="0.45"/></svg>'),
        "Wooden Bed": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#efebe9"/><rect x="60" y="72" width="28" height="170" rx="6" fill="#5d4037"/><rect x="312" y="72" width="28" height="170" rx="6" fill="#5d4037"/><rect x="60" y="178" width="280" height="65" rx="6" fill="#8d6e63"/><rect x="60" y="130" width="280" height="52" rx="4" fill="#bcaaa4"/><rect x="76" y="95" width="48" height="38" rx="4" fill="#ffecb3"/><rect x="176" y="95" width="48" height="38" rx="4" fill="#ffecb3"/></svg>'),
        "Office Chair": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#f3e5f5"/><rect x="155" y="55" width="90" height="115" rx="12" fill="#212121"/><rect x="163" y="63" width="74" height="99" rx="8" fill="#424242"/><rect x="158" y="170" width="84" height="18" rx="5" fill="#333"/><rect x="196" y="188" width="8" height="48" rx="3" fill="#555"/><ellipse cx="200" cy="240" rx="44" ry="8" fill="#333"/><line x1="156" y1="238" x2="200" y2="238" stroke="#444" stroke-width="5" stroke-linecap="round"/><line x1="244" y1="238" x2="200" y2="238" stroke="#444" stroke-width="5" stroke-linecap="round"/><line x1="156" y1="238" x2="141" y2="258" stroke="#444" stroke-width="5" stroke-linecap="round"/><line x1="244" y1="238" x2="259" y2="258" stroke="#444" stroke-width="5" stroke-linecap="round"/><circle cx="141" cy="260" r="7" fill="#222"/><circle cx="259" cy="260" r="7" fill="#222"/><circle cx="200" cy="244" r="7" fill="#222"/></svg>'),
        "Nike Running Shoes": _b64(_SK.replace("{u}", "#111").replace("{sl}", "#e5282a")),
        "Adidas Sneakers": _b64(_SK.replace("{u}", "#f5f5f5").replace("{sl}", "#000")),
        "Puma Sports Shoes": _b64(_SK.replace("{u}", "#e53935").replace("{sl}", "#111")),
        "Levi's Jeans": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e8eaf6"/><rect x="150" y="50" width="100" height="28" rx="4" fill="#1a237e"/><path d="M150 78 L130 270 L185 270 L200 162 L215 270 L270 270 L250 78 Z" fill="#1565c0"/><line x1="200" y1="78" x2="200" y2="270" stroke="#0d47a1" stroke-width="3"/><rect x="165" y="87" width="24" height="16" rx="3" fill="#0d47a1"/></svg>'),
        "Zara T-Shirt": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fce4ec"/><path d="M140 80 L100 120 L130 135 L130 250 L270 250 L270 135 L300 120 L260 80 Q230 65 200 65 Q170 65 140 80 Z" fill="#e91e63"/><path d="M140 80 Q170 65 200 65 Q230 65 260 80 Q240 95 220 90 L200 108 L180 90 Q160 95 140 80 Z" fill="#c2185b"/></svg>'),
        "H&M Hoodie": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e8f5e9"/><path d="M140 75 L95 130 L130 145 L130 260 L270 260 L270 145 L305 130 L260 75 Q230 60 200 60 Q170 60 140 75 Z" fill="#388e3c"/><path d="M140 75 Q170 60 200 60 Q230 60 260 75 L240 100 Q220 115 200 110 Q180 115 160 100 Z" fill="#2e7d32"/><rect x="185" y="108" width="30" height="38" rx="5" fill="#1b5e20"/></svg>'),
    }
    _CAT_FB = {
        "Electronics": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e8eaf6"/><rect x="100" y="80" width="200" height="130" rx="10" fill="#3f51b5"/><rect x="110" y="90" width="180" height="110" rx="6" fill="#c5cae9"/><rect x="160" y="210" width="80" height="12" rx="4" fill="#9fa8da"/></svg>'),
        "Footwear": _b64(_SK.replace("{u}", "#5c6bc0").replace("{sl}", "#283593")),
        "Clothing": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#fce4ec"/><path d="M145 80 L105 118 L135 132 L135 248 L265 248 L265 132 L295 118 L255 80 Q225 66 200 66 Q175 66 145 80 Z" fill="#ec407a"/><path d="M145 80 Q175 66 200 66 Q225 66 255 80 Q235 96 215 91 L200 108 L185 91 Q165 96 145 80 Z" fill="#c2185b"/></svg>'),
        "Furniture": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#efebe9"/><rect x="80" y="130" width="240" height="70" rx="8" fill="#795548"/><rect x="80" y="200" width="240" height="20" rx="4" fill="#6d4c41"/><rect x="90" y="220" width="20" height="50" rx="4" fill="#5d4037"/><rect x="290" y="220" width="20" height="50" rx="4" fill="#5d4037"/><rect x="80" y="80" width="240" height="55" rx="8" fill="#a1887f"/></svg>'),
        "Home Appliances": _b64('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#e8f5e9"/><rect x="130" y="60" width="140" height="180" rx="10" fill="#eceff1"/><rect x="140" y="70" width="120" height="160" rx="6" fill="#fff"/><circle cx="200" cy="160" r="50" fill="#b0bec5"/><circle cx="200" cy="160" r="38" fill="#e3f2fd"/></svg>'),
    }

    def get_product_image(product_name: str, category: str) -> str:
        if product_name in _PRODUCT_IMAGES:
            return _PRODUCT_IMAGES[product_name]
        for key in _PRODUCT_IMAGES:
            if key.lower() in product_name.lower() or product_name.lower() in key.lower():
                return _PRODUCT_IMAGES[key]
        return _CAT_FB.get(category, _CAT_FB["Electronics"])

    def parse_nl_filters(query):
        filters = {}
        original = query
        price_pat = re.search(
            r'(under|below|less\s+than|upto|up\s+to)\s*[₹rs\.]*\s*(\d[\d,]*)\s*k?',
            query, re.I
        )
        if price_pat:
            raw = price_pat.group(2).replace(",", "")
            val = int(raw) * 1000 if "k" in price_pat.group(0).lower()[-2:] else int(raw)
            filters["max_price"] = val
            query = query[:price_pat.start()].strip()
        cat_map = {
            "laptop": "Electronics", "phone": "Electronics", "mobile": "Electronics",
            "iphone": "Electronics", "samsung": "Electronics", "headphone": "Electronics",
            "tv": "Electronics", "shoe": "Footwear", "sneaker": "Footwear",
            "boot": "Footwear", "sandal": "Footwear", "shirt": "Clothing",
            "dress": "Clothing", "jeans": "Clothing", "trouser": "Clothing",
            "jacket": "Clothing", "cloth": "Clothing", "sofa": "Furniture",
            "chair": "Furniture", "table": "Furniture", "bed": "Furniture",
            "furniture": "Furniture", "washing": "Home Appliances",
            "fridge": "Home Appliances", "refrigerator": "Home Appliances",
            "appliance": "Home Appliances", "microwave": "Home Appliances",
        }
        for kw, cat in cat_map.items():
            if kw in original.lower():
                filters["category"] = cat
                break
        return query.strip() or original.strip(), filters

    def get_similar_products(idx, top_n=5):
        sims = item_sim[idx]
        top_idx = sims.argsort()[::-1][1: top_n + 1]
        return df.iloc[top_idx][["product_name", "category", "price"]].to_dict("records")

    def hybrid_search(query, alpha, threshold, cat_filter, price_min, price_max, sort_by, use_rerank):
        query = query.strip().lower()
        if not query:
            return pd.DataFrame()

        # FIX 1: Direct keyword fallback — always include exact name matches regardless of score
        keyword_mask = df["search_text"].str.contains(re.escape(query), case=False, na=False)

        fuzzy_hits = fuzz_process.extract(query, df["search_text"].tolist(), limit=5, score_cutoff=40)
        all_queries = [query] + [h[0] for h in fuzzy_hits]
        qvec = vectorizer.transform(all_queries)
        tfidf_scores = cosine_similarity(qvec, tfidf_mat).max(axis=0)
        qlsa = svd.transform(qvec)
        sem_scores = cosine_similarity(qlsa, lsa_mat).max(axis=0)
        hybrid = alpha * tfidf_scores + (1 - alpha) * sem_scores

        # Boost direct keyword matches so they always surface
        hybrid[keyword_mask.values] = np.maximum(hybrid[keyword_mask.values], threshold + 0.1)

        if use_rerank:
            boost = 1 + 0.15 * df["popularity_score"].values
            hybrid = hybrid * boost
        results = df.copy()
        results["tfidf_score"] = (tfidf_scores * 100).round(1)
        results["semantic_score"] = (sem_scores * 100).round(1)
        results["similarity"] = hybrid
        results = results[results["similarity"] >= threshold]
        if cat_filter != "All":
            results = results[results["category"] == cat_filter]
        results = results[(results["price"] >= price_min) & (results["price"] <= price_max)]
        if sort_by == "Best match":
            results = results.sort_values("similarity", ascending=False)
        elif sort_by == "Price: low → high":
            results = results.sort_values("price")
        elif sort_by == "Price: high → low":
            results = results.sort_values("price", ascending=False)
        return results.head(50).reset_index()

    def ab_compare(query, threshold=0.1):
        query_l = query.strip().lower()
        if not query_l:
            return None, None, {}
        qvec = vectorizer.transform([query_l])
        t_scores = cosine_similarity(qvec, tfidf_mat).flatten()
        res_a = df.copy()
        res_a["similarity"] = t_scores
        res_a = res_a[res_a["similarity"] >= threshold].sort_values("similarity", ascending=False).head(5)
        res_b = hybrid_search(query, alpha=0.5, threshold=threshold,
                              cat_filter="All", price_min=PRICE_MIN, price_max=PRICE_MAX,
                              sort_by="Best match", use_rerank=True).head(5)
        def precision_at_k(results, k=5):
            if results.empty: return 0.0
            return round(len(results.head(k)) / k * 100, 1)
        def avg_score(results):
            if results.empty: return 0.0
            return round(float(results["similarity"].mean()) * 100, 1)
        metrics = {
            "TF-IDF results": len(res_a),
            "Hybrid results": len(res_b),
            "TF-IDF avg score": avg_score(res_a),
            "Hybrid avg score": avg_score(res_b),
            "TF-IDF P@5": precision_at_k(res_a),
            "Hybrid P@5": precision_at_k(res_b),
        }
        return res_a, res_b, metrics

    # ══════════════════════════════════════════════════════════════════════════
    # SESSION STATE
    # ══════════════════════════════════════════════════════════════════════════
    if "search_log" not in st.session_state:
        st.session_state.search_log = []
    if "recent_queries" not in st.session_state:
        st.session_state.recent_queries = []
    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

    # ══════════════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ══════════════════════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("### ⚙ Filters & controls")
        # Cache clear button — press this if search shows no results after fixing CSV
        if st.button("🔄 Reload data", help="Press if search is broken or you changed the CSV"):
            st.cache_resource.clear()
            st.rerun()
        selected_category = st.selectbox("Category", CATEGORIES)
        price_range = st.slider("Price range (₹)", PRICE_MIN, PRICE_MAX,
                                (PRICE_MIN, PRICE_MAX), step=500, format="₹%d")
        sort_by = st.selectbox("Sort by", ["Best match", "Price: low → high", "Price: high → low"])
        st.markdown("---")
        st.markdown("### 🧠 Model controls")
        alpha = st.slider("TF-IDF ↔ Semantic weight (alpha)", 0.0, 1.0, 0.5, step=0.05,
                          help="0 = pure semantic search | 1 = pure TF-IDF keyword search")
        threshold = st.slider("Match threshold", 0.01, 0.80, 0.05, step=0.01)
        use_rerank = st.toggle("Popularity re-ranking", value=True)
        show_explain = st.toggle("Show match explanation", value=True)
        show_similar = st.toggle("Show similar products", value=True)
        if st.session_state.recent_queries:
            st.markdown("---")
            st.markdown("### 🕐 Recent searches")
            for q in st.session_state.recent_queries[-5:][::-1]:
                if st.button(f"↩ {q}", key=f"rc_{q}"):
                    st.session_state.query_input = q
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════════════════════════════════════
    tab_search, tab_ab, tab_analytics, tab_insights = st.tabs([
        "🔍 Search", "⚖ A/B Test", "📊 Analytics", "🧠 Model insights"
    ])

    # ── TAB 1: SEARCH ─────────────────────────────────────────────────────────
    with tab_search:
        st.markdown(f"""
        <div class="search-hero">
            <div class="hero-title">SmartFind</div>
            <div class="hero-sub">Hybrid TF-IDF + Semantic AI product search engine</div>
            <div class="hero-stats">
                <div class="hero-stat"><span>{len(df):,}</span> products</div>
                <div class="hero-stat"><span>{len(CATEGORIES) - 1}</span> categories</div>
                <div class="hero-stat"><span>LSA Semantic</span> embeddings</div>
                <div class="hero-stat"><span>NL filters</span> auto-detected</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        query_raw = st.text_input(
            "Search",
            value=st.session_state.query_input,
            placeholder='Try: "laptops under 60000" or "running shoes" or "wooden sofa"…',
            label_visibility="collapsed",
            key="query_input",
        )

        col1, col2 = st.columns([1, 7])
        with col1:
            search_btn = st.button("Search", type="primary", use_container_width=True)

        if search_btn and query_raw.strip():
            clean_query, nl_filters = parse_nl_filters(query_raw)
            effective_cat = nl_filters.get("category", selected_category)
            effective_max_price = min(nl_filters.get("max_price", price_range[1]), price_range[1])

            if nl_filters:
                tags = ""
                if "category" in nl_filters:
                    tags += f'<span class="nl-tag">📂 {nl_filters["category"]}</span>'
                if "max_price" in nl_filters:
                    tags += f'<span class="nl-tag">💰 Under ₹{nl_filters["max_price"]:,}</span>'
                st.markdown(f'<div style="margin-bottom:0.7rem">Auto-detected filters: {tags}</div>',
                            unsafe_allow_html=True)

            if query_raw not in st.session_state.recent_queries:
                st.session_state.recent_queries.append(query_raw)

            with st.spinner("Searching with hybrid AI engine…"):
                results = hybrid_search(
                    clean_query, alpha, threshold,
                    effective_cat, price_range[0], effective_max_price,
                    sort_by, use_rerank
                )

            st.session_state.search_log.append({
                "query": query_raw, "clean": clean_query,
                "results": len(results), "category": effective_cat,
            })

            if results.empty:
                st.warning("No products found.")
                # Debug expander to diagnose the issue
                with st.expander("🔍 Debug info — why no results?"):
                    query_lower = clean_query.strip().lower()
                    keyword_matches = df["search_text"].str.contains(re.escape(query_lower), case=False, na=False).sum()
                    st.write(f"**Query sent to engine:** `{clean_query}`")
                    st.write(f"**Category filter applied:** `{effective_cat}`")
                    st.write(f"**Price range:** ₹{price_range[0]:,} – ₹{effective_max_price:,}")
                    st.write(f"**Threshold:** `{threshold}`")
                    st.write(f"**Products matching keyword in search_text:** `{keyword_matches}`")
                    st.write(f"**Total products in dataset:** `{len(df)}`")
                    st.write("**Sample product names in dataset:**")
                    st.write(df["product_name"].sample(min(10, len(df))).tolist())
            else:
                st.write(f"**{len(results)} results** for **'{query_raw}'** · alpha={alpha} · threshold={threshold}")
                st.divider()

                cols = st.columns(4)
                for rank, (_, row) in enumerate(results.iterrows(), 1):
                    col_idx = (rank - 1) % 4
                    with cols[col_idx]:
                        # FIX 3: Use real image URL from CSV, fall back to SVG placeholder
                        img_url = str(row.get("image_url", "")).strip()
                        # Only use URL if it looks valid (starts with http)
                        if img_url and img_url.lower().startswith("http"):
                            try:
                                st.image(img_url, use_container_width=True)
                            except Exception:
                                st.image(get_product_image(row["product_name"], row["category"]),
                                         use_container_width=True)
                        else:
                            st.image(get_product_image(row["product_name"], row["category"]),
                                     use_container_width=True)

                        # Rank badge
                        rank_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")

                        # FIX 2: Native Streamlit components — no raw HTML
                        st.markdown(f"**{rank_emoji} {row['product_name'][:55]}{'...' if len(str(row['product_name'])) > 55 else ''}**")

                        brand = str(row.get("brand", "")).strip()
                        if brand and brand != "Unknown":
                            st.caption(f"🏷 {brand}  ·  {row['category']}")
                        else:
                            st.caption(f"📂 {row['category']}")

                        # Rating stars
                        try:
                            rating_val = float(row["rating"])
                            stars = "★" * int(round(rating_val)) + "☆" * (5 - int(round(rating_val)))
                            st.caption(f"{stars} {rating_val:.1f}")
                        except Exception:
                            pass

                        # Price row
                        ret = row.get("retail_price", row["price"])
                        try:
                            disc_pct = round((1 - row["price"] / float(ret)) * 100)
                        except Exception:
                            disc_pct = 0

                        price_str = f"₹{int(row['price']):,}"
                        if disc_pct >= 5:
                            st.markdown(f"**{price_str}** 🔴 `{disc_pct}% off`")
                        else:
                            st.markdown(f"**{price_str}**")
                        st.caption(f"AI est: ₹{int(row['predicted_price']):,}  ·  {CLUSTER_NAMES.get(int(row['cluster']), 'Group')}")

                        # Match score bar using st.progress
                        score_pct = round(float(row["similarity"]) * 100, 1)
                        st.progress(min(score_pct / 100, 1.0), text=f"Match {score_pct}%")
                        st.caption(f"TF-IDF {row['tfidf_score']}%  ·  LSA {row['semantic_score']}%")

                        # Similar products
                        if show_similar:
                            orig_idx = int(row["index"]) if "index" in row else row.name
                            similar = get_similar_products(orig_idx, top_n=3)
                            if similar:
                                with st.expander("🔗 Similar products"):
                                    for s in similar:
                                        st.write(f"• {s['product_name'][:30]} — ₹{int(s['price']):,}")

                        st.divider()

                st.download_button(
                    "⬇ Export results as CSV",
                    data=results[["product_name", "category", "price",
                                  "tfidf_score", "semantic_score", "similarity"]].to_csv(index=False),
                    file_name=f"results_{clean_query.replace(' ', '_')}.csv",
                    mime="text/csv",
                )

        elif search_btn:
            st.warning("Please enter a search term.")

    # ── TAB 2: A/B TEST ───────────────────────────────────────────────────────
    with tab_ab:
        st.subheader("A/B test: TF-IDF only vs Hybrid search")
        st.caption("Runs the same query through two ranking algorithms side-by-side and measures result quality.")

        ab_query = st.text_input("Enter a query to test", placeholder="e.g. running shoes", key="ab_query")
        ab_btn = st.button("Run A/B test", type="primary")

        if ab_btn and ab_query.strip():
            res_a, res_b, metrics = ab_compare(ab_query, threshold=0.05)
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown('<div class="ab-col">', unsafe_allow_html=True)
                st.markdown('<div class="ab-title">Algorithm A — TF-IDF only</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="ab-metric"><span>Results found</span><span>{metrics['TF-IDF results']}</span></div>
                <div class="ab-metric"><span>Avg match score</span><span>{metrics['TF-IDF avg score']}%</span></div>
                <div class="ab-metric"><span>Precision@5</span><span>{metrics['TF-IDF P@5']}%</span></div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if res_a is not None and not res_a.empty:
                    st.dataframe(
                        res_a[["product_name", "category", "price", "similarity"]]
                        .rename(columns={"similarity": "score"}).head(5),
                        hide_index=True, use_container_width=True
                    )
            with col_m2:
                st.markdown('<div class="ab-col">', unsafe_allow_html=True)
                st.markdown('<div class="ab-title">Algorithm B — Hybrid (TF-IDF + Semantic + Re-rank)</div>',
                            unsafe_allow_html=True)
                winner = metrics["Hybrid avg score"] >= metrics["TF-IDF avg score"]
                win_tag = ' <span class="ab-win">▲ winner</span>' if winner else ""
                st.markdown(f"""
                <div class="ab-metric"><span>Results found</span><span>{metrics['Hybrid results']}{win_tag if metrics['Hybrid results'] >= metrics['TF-IDF results'] else ''}</span></div>
                <div class="ab-metric"><span>Avg match score</span><span>{metrics['Hybrid avg score']}%{win_tag if winner else ''}</span></div>
                <div class="ab-metric"><span>Precision@5</span><span>{metrics['Hybrid P@5']}%{win_tag if metrics['Hybrid P@5'] >= metrics['TF-IDF P@5'] else ''}</span></div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                if res_b is not None and not res_b.empty:
                    st.dataframe(
                        res_b[["product_name", "category", "price", "similarity"]]
                        .rename(columns={"similarity": "score"}).head(5),
                        hide_index=True, use_container_width=True
                    )
            st.info("**Interview talking point:** This is offline evaluation of ranking algorithms. "
                    "In industry, metrics like Precision@K, NDCG, and MRR decide which algorithm to deploy.")
        elif ab_btn:
            st.warning("Enter a query first.")

    # ── TAB 3: ANALYTICS ──────────────────────────────────────────────────────
    with tab_analytics:
        st.subheader("Search analytics")
        log = st.session_state.search_log
        total = len(log)
        zero = sum(1 for l in log if l["results"] == 0)
        avg_r = round(sum(l["results"] for l in log) / total, 1) if total else 0
        zero_r = round(zero / total * 100, 1) if total else 0

        st.markdown(f"""
        <div class="analytics-grid">
            <div class="analytics-card">
                <div class="analytics-label">Total searches</div>
                <div class="analytics-value">{total}</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-label">Avg results returned</div>
                <div class="analytics-value">{avg_r}</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-label">Zero-result rate</div>
                <div class="analytics-value">{zero_r}%</div>
            </div>
            <div class="analytics-card">
                <div class="analytics-label">Products indexed</div>
                <div class="analytics-value">{len(df):,}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if log:
            col_t, col_h = st.columns(2)
            with col_t:
                st.markdown("#### Top queries this session")
                qc = collections.Counter(l["query"] for l in log)
                rows = "".join(
                    f'<div class="trend-item"><span>{q}</span><span class="trend-count">{c}x</span></div>'
                    for q, c in qc.most_common(8)
                )
                st.markdown(
                    f'<div style="background:#fff;border:1px solid #e8e8f0;border-radius:12px;padding:1rem">{rows}</div>',
                    unsafe_allow_html=True)
            with col_h:
                st.markdown("#### Search history")
                st.dataframe(pd.DataFrame(log), hide_index=True, use_container_width=True)
        else:
            st.info("Run searches on the Search tab to populate analytics.")

        st.markdown("#### Dataset overview by category")
        # ── FIX 7: Use product_name instead of product_id (may not exist) ────
        count_col = "product_name" if "product_name" in df.columns else df.columns[0]
        cat_df = df.groupby("category").agg(
            Count=(count_col, "count"),
            Avg_Price=("price", lambda x: f"₹{int(x.mean()):,}"),
            Min_Price=("price", lambda x: f"₹{int(x.min()):,}"),
            Max_Price=("price", lambda x: f"₹{int(x.max()):,}"),
        ).reset_index()
        st.dataframe(cat_df, hide_index=True, use_container_width=True)

        st.markdown("#### Cluster distribution")
        cluster_df = df.groupby("cluster").agg(
            Name=("cluster", lambda x: CLUSTER_NAMES.get(int(x.iloc[0]), "Group")),
            Products=(count_col, "count"),
            Avg_Price=("price", lambda x: f"₹{int(x.mean()):,}"),
        ).reset_index(drop=True)
        st.dataframe(cluster_df, hide_index=True, use_container_width=True)

    # ── TAB 4: MODEL INSIGHTS ─────────────────────────────────────────────────
    with tab_insights:
        st.subheader("Model insights")
        st.caption("Everything happening under the hood — useful for interviews.")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### Search engine")
            st.markdown(f"""
            <div class="analytics-card">
            <div class="insight-row"><span class="insight-key">TF-IDF vocabulary</span><span class="insight-val">{len(vectorizer.vocabulary_):,} terms</span></div>
            <div class="insight-row"><span class="insight-key">N-gram range</span><span class="insight-val">(1, 2)</span></div>
            <div class="insight-row"><span class="insight-key">Semantic model</span><span class="insight-val">LSA / TruncatedSVD</span></div>
            <div class="insight-row"><span class="insight-key">LSA dimensions</span><span class="insight-val">50 components</span></div>
            <div class="insight-row"><span class="insight-key">Fuzzy matching</span><span class="insight-val">rapidfuzz Levenshtein</span></div>
            <div class="insight-row"><span class="insight-key">Hybrid alpha</span><span class="insight-val">{alpha} (sidebar)</span></div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### Price prediction model")
            preds = rf.predict(df[["cat_enc", "brand_enc"]])
            r2 = round(r2_score(df["price"], preds), 3)
            mae = round(mean_absolute_error(df["price"], preds))
            st.markdown(f"""
            <div class="analytics-card">
            <div class="insight-row"><span class="insight-key">Algorithm</span><span class="insight-val">Random Forest</span></div>
            <div class="insight-row"><span class="insight-key">Estimators</span><span class="insight-val">100 trees</span></div>
            <div class="insight-row"><span class="insight-key">Features</span><span class="insight-val">category + brand</span></div>
            <div class="insight-row"><span class="insight-key">R² score</span><span class="insight-val">{r2}</span></div>
            <div class="insight-row"><span class="insight-key">MAE</span><span class="insight-val">₹{mae:,}</span></div>
            </div>""", unsafe_allow_html=True)

        with col_b:
            st.markdown("#### Clustering")
            st.markdown(f"""
            <div class="analytics-card">
            <div class="insight-row"><span class="insight-key">Algorithm</span><span class="insight-val">KMeans</span></div>
            <div class="insight-row"><span class="insight-key">Clusters</span><span class="insight-val">8</span></div>
            <div class="insight-row"><span class="insight-key">Input features</span><span class="insight-val">LSA 50-dim embeddings</span></div>
            <div class="insight-row"><span class="insight-key">Documents</span><span class="insight-val">{len(df):,}</span></div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### Top TF-IDF terms per category")
            for cat in sorted(df["category"].unique()):
                sub = df[df["category"] == cat]
                sub_mat = vectorizer.transform(sub["search_text"])
                mean_scores = sub_mat.mean(axis=0).A1
                top_idx = mean_scores.argsort()[::-1][:6]
                terms = ", ".join(FEAT_NAMES[i] for i in top_idx)
                st.markdown(f"**{cat}** — `{terms}`")

        st.markdown("#### Live explainability test")
        st.caption("Type any query to see which TF-IDF terms would drive its match score.")
        exp_q = st.text_input("Test query for explanation", placeholder="e.g. laptop")
        if exp_q.strip():
            qvec_test = vectorizer.transform([exp_q.lower()]).toarray()[0]
            top_terms_idx = qvec_test.argsort()[::-1][:10]
            top_terms = [(FEAT_NAMES[i], round(float(qvec_test[i]), 4))
                         for i in top_terms_idx if qvec_test[i] > 0]
            if top_terms:
                chips = "".join(
                    f'<span class="explain-term">{t} ({v})</span>'
                    for t, v in top_terms
                )
                st.markdown(f"<div style='margin-top:0.5rem'>{chips}</div>", unsafe_allow_html=True)
            else:
                st.info("No matching terms found in vocabulary.")