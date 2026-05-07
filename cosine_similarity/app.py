import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process as fuzz_process
import math

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartFind – Product Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

/* ── Hero search bar ── */
.search-hero {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0d1b2a 100%);
    border-radius: 20px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(99,102,241,0.3);
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 600;
    color: #fff;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.55);
    margin-bottom: 1.8rem;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.5rem;
}
.hero-stat {
    color: rgba(255,255,255,0.6);
    font-size: 0.82rem;
}
.hero-stat span {
    color: #a5b4fc;
    font-weight: 600;
    font-size: 1rem;
}

/* ── Product cards ── */
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.product-card {
    background: #fff;
    border: 1px solid #e8e8f0;
    border-radius: 14px;
    padding: 1.2rem;
    transition: box-shadow .2s, transform .2s;
    position: relative;
    overflow: hidden;
}
.product-card:hover {
    box-shadow: 0 8px 30px rgba(99,102,241,0.12);
    transform: translateY(-2px);
}
.card-category {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem;
    padding: 3px 8px;
    border-radius: 20px;
    display: inline-block;
}
.cat-Electronics    { background:#ede9fe; color:#5b21b6; }
.cat-Clothing       { background:#fce7f3; color:#9d174d; }
.cat-Footwear       { background:#fef3c7; color:#92400e; }
.cat-Furniture      { background:#d1fae5; color:#065f46; }
.cat-Home           { background:#dbeafe; color:#1e40af; }
.product-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.8rem;
    line-height: 1.4;
}
.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: 0.8rem;
}
.product-price {
    font-size: 1.1rem;
    font-weight: 600;
    color: #111827;
    font-family: 'DM Mono', monospace;
}
.match-section { margin-top: 0.7rem; }
.match-label {
    font-size: 0.72rem;
    color: #6b7280;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
}
.match-bar-bg {
    height: 5px;
    background: #f3f4f6;
    border-radius: 99px;
    overflow: hidden;
}
.match-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width .4s ease;
}
.rank-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #f3f4f6;
    color: #374151;
    font-size: 0.72rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
}
.rank-1 { background: #fef3c7; color: #92400e; }
.rank-2 { background: #f3f4f6; color: #374151; }
.rank-3 { background: #fce7f3; color: #9d174d; }

/* ── Result header ── */
.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #f0f0f5;
}
.result-count {
    font-size: 0.9rem;
    color: #6b7280;
}
.result-count strong { color: #111827; }

/* ── Sidebar ── */
.sidebar-section {
    margin-bottom: 1.5rem;
}
.sidebar-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #9ca3af;
    margin-bottom: 0.6rem;
}

/* ── No results ── */
.no-results {
    text-align: center;
    padding: 4rem 2rem;
    color: #9ca3af;
}
.no-results-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #374151;
    margin-bottom: 0.5rem;
}

/* ── Analytics cards ── */
.analytics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.analytics-card {
    background: #fff;
    border: 1px solid #e8e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
}
.analytics-label {
    font-size: 0.78rem;
    color: #6b7280;
    margin-bottom: 0.3rem;
}
.analytics-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: #111827;
    font-family: 'DM Mono', monospace;
}
.analytics-delta {
    font-size: 0.78rem;
    color: #059669;
    margin-top: 0.2rem;
}

/* ── Model insights ── */
.insight-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f3f4f6;
    font-size: 0.88rem;
}
.insight-row:last-child { border-bottom: none; }
.insight-key { color: #374151; font-weight: 500; }
.insight-val { color: #6366f1; font-weight: 600; font-family: 'DM Mono', monospace; }
</style>
""", unsafe_allow_html=True)


# ── Data & model (cached) ──────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    df = pd.read_csv("real product.csv")
    # Normalise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # Build rich search text: name + category (weight name more by repeating it)
    df["search_text"] = (
        df["product_name"].str.lower() + " " +
        df["product_name"].str.lower() + " " +
        df["category"].str.lower()
    )
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,       # dampen very frequent terms
    )
    matrix = vectorizer.fit_transform(df["search_text"])
    return df, vectorizer, matrix


# ── Search function ────────────────────────────────────────────────────────────
def search_products(query: str, category_filter: str, price_min: float,
                    price_max: float, sort_by: str, threshold: float,
                    df, vectorizer, matrix):
    # FIX 1: actually use lowercased query
    query = query.strip().lower()

    # FIX 2: empty guard
    if not query:
        return pd.DataFrame()

    # Fuzzy expand: get close matches from search_text pool
    all_texts = df["search_text"].tolist()
    fuzzy_hits = fuzz_process.extract(query, all_texts, limit=5, score_cutoff=40)
    extra_queries = [hit[0] for hit in fuzzy_hits]
    all_queries = [query] + extra_queries

    query_vec = vectorizer.transform(all_queries)
    scores = cosine_similarity(query_vec, matrix).max(axis=0)

    # FIX 3: work on a copy, never mutate global df
    results = df.copy()
    results["similarity"] = scores

    # FIX 4: sensible threshold (was 0.9 — almost nothing ever scored that high)
    results = results[results["similarity"] >= threshold]

    # Apply filters
    if category_filter != "All":
        results = results[results["category"] == category_filter]
    results = results[
        (results["price"] >= price_min) & (results["price"] <= price_max)
    ]

    # Sort
    if sort_by == "Best match":
        results = results.sort_values("similarity", ascending=False)
    elif sort_by == "Price: low → high":
        results = results.sort_values("price", ascending=True)
    elif sort_by == "Price: high → low":
        results = results.sort_values("price", ascending=False)

    return results.head(50)


# ── Search session log (in-memory) ────────────────────────────────────────────
if "search_log" not in st.session_state:
    st.session_state.search_log = []
if "recent_queries" not in st.session_state:
    st.session_state.recent_queries = []


# ── Load model ────────────────────────────────────────────────────────────────
df, vectorizer, matrix = load_model()

CATEGORIES = ["All"] + sorted(df["category"].unique().tolist())
PRICE_MIN = int(df["price"].min())
PRICE_MAX = int(df["price"].max())


# ── Category colour helper ─────────────────────────────────────────────────────
def cat_class(cat: str) -> str:
    mapping = {
        "Electronics": "cat-Electronics",
        "Clothing": "cat-Clothing",
        "Footwear": "cat-Footwear",
        "Furniture": "cat-Furniture",
        "Home Appliances": "cat-Home",
    }
    return mapping.get(cat, "cat-Home")


# ── Match-bar colour ───────────────────────────────────────────────────────────
def bar_colour(score: float) -> str:
    if score >= 0.7:
        return "#10b981"
    if score >= 0.4:
        return "#6366f1"
    return "#f59e0b"


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### Filters")

    st.markdown('<div class="sidebar-title">Category</div>', unsafe_allow_html=True)
    selected_category = st.selectbox("", CATEGORIES, label_visibility="collapsed")

    st.markdown('<div class="sidebar-title">Price range (₹)</div>', unsafe_allow_html=True)
    price_range = st.slider("", PRICE_MIN, PRICE_MAX,
                            (PRICE_MIN, PRICE_MAX), step=500,
                            label_visibility="collapsed",
                            format="₹%d")

    st.markdown('<div class="sidebar-title">Sort by</div>', unsafe_allow_html=True)
    sort_by = st.selectbox("", ["Best match", "Price: low → high", "Price: high → low"],
                           label_visibility="collapsed")

    st.markdown('<div class="sidebar-title">Match threshold</div>', unsafe_allow_html=True)
    threshold = st.slider("", 0.05, 0.80, 0.15, step=0.05,
                          label_visibility="collapsed")

    # Recent searches
    if st.session_state.recent_queries:
        st.markdown("---")
        st.markdown("### Recent searches")
        for q in st.session_state.recent_queries[-5:][::-1]:
            if st.button(f"↩ {q}", key=f"recent_{q}"):
                st.session_state["query_input"] = q


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_search, tab_analytics, tab_insights = st.tabs(["Search", "Analytics", "Model insights"])


# ── TAB 1: SEARCH ─────────────────────────────────────────────────────────────
with tab_search:
    # Hero
    st.markdown(f"""
    <div class="search-hero">
        <div class="hero-title">SmartFind</div>
        <div class="hero-sub">AI-powered product discovery engine</div>
        <div class="hero-stats">
            <div class="hero-stat"><span>{len(df):,}</span> products indexed</div>
            <div class="hero-stat"><span>{len(CATEGORIES)-1}</span> categories</div>
            <div class="hero-stat"><span>TF-IDF + Fuzzy</span> ranking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search input
    query = st.text_input(
        "Search products…",
        value=st.session_state.get("query_input", ""),
        placeholder="e.g. Samsung washing machine, running shoes, wooden chair…",
        key="query_input",
    )

    col_btn, col_clear = st.columns([1, 6])
    with col_btn:
        search_clicked = st.button("Search", type="primary", use_container_width=True)

    # Run search
    if search_clicked and query.strip():
        # Save to recent
        if query not in st.session_state.recent_queries:
            st.session_state.recent_queries.append(query)

        with st.spinner("Finding best matches…"):
            results = search_products(
                query, selected_category,
                price_range[0], price_range[1],
                sort_by, threshold,
                df, vectorizer, matrix,
            )

        # Log for analytics
        st.session_state.search_log.append({
            "query": query,
            "results": len(results),
            "category": selected_category,
        })

        if results.empty:
            st.markdown("""
            <div class="no-results">
                <div class="no-results-title">No products found</div>
                <p>Try lowering the match threshold in the sidebar, or use a broader search term.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Result header
            st.markdown(f"""
            <div class="result-header">
                <div class="result-count">
                    Showing <strong>{len(results)}</strong> results for
                    <strong>"{query}"</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Product cards grid
            cards_html = '<div class="product-grid">'
            for rank, (_, row) in enumerate(results.iterrows(), 1):
                score_pct = round(row["similarity"] * 100, 1)
                price_fmt = f"₹{int(row['price']):,}"
                cat = row["category"]
                rank_class = f"rank-{min(rank, 3)}"
                colour = bar_colour(row["similarity"])

                cards_html += f"""
                <div class="product-card">
                    <div class="rank-badge {rank_class}">#{rank}</div>
                    <div class="card-category {cat_class(cat)}">{cat}</div>
                    <div class="product-name">{row['product_name']}</div>
                    <div class="card-footer">
                        <div class="product-price">{price_fmt}</div>
                    </div>
                    <div class="match-section">
                        <div class="match-label">
                            <span>Match score</span>
                            <span>{score_pct}%</span>
                        </div>
                        <div class="match-bar-bg">
                            <div class="match-bar-fill"
                                 style="width:{score_pct}%; background:{colour};">
                            </div>
                        </div>
                    </div>
                </div>
                """
            cards_html += "</div>"
            st.markdown(cards_html, unsafe_allow_html=True)

            # Download
            st.download_button(
                "⬇ Export results as CSV",
                data=results[["product_name", "category", "price", "similarity"]].to_csv(index=False),
                file_name=f"results_{query.replace(' ','_')}.csv",
                mime="text/csv",
            )

    elif not query.strip() and search_clicked:
        st.warning("Please enter a search term.")


# ── TAB 2: ANALYTICS ──────────────────────────────────────────────────────────
with tab_analytics:
    st.subheader("Search analytics")

    log = st.session_state.search_log
    total_searches = len(log)
    zero_result = sum(1 for l in log if l["results"] == 0)
    avg_results = round(sum(l["results"] for l in log) / total_searches, 1) if total_searches else 0
    zero_rate = round(zero_result / total_searches * 100, 1) if total_searches else 0

    st.markdown(f"""
    <div class="analytics-grid">
        <div class="analytics-card">
            <div class="analytics-label">Total searches</div>
            <div class="analytics-value">{total_searches}</div>
        </div>
        <div class="analytics-card">
            <div class="analytics-label">Avg results returned</div>
            <div class="analytics-value">{avg_results}</div>
        </div>
        <div class="analytics-card">
            <div class="analytics-label">Zero-result rate</div>
            <div class="analytics-value">{zero_rate}%</div>
        </div>
        <div class="analytics-card">
            <div class="analytics-label">Products indexed</div>
            <div class="analytics-value">{len(df):,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if log:
        import collections
        st.markdown("#### Top queries this session")
        q_counts = collections.Counter(l["query"] for l in log)
        q_df = pd.DataFrame(q_counts.most_common(10), columns=["Query", "Count"])
        st.dataframe(q_df, hide_index=True, use_container_width=True)

        st.markdown("#### Search history")
        log_df = pd.DataFrame(log)
        log_df.index += 1
        st.dataframe(log_df, use_container_width=True)
    else:
        st.info("Run some searches on the Search tab to see analytics here.")

    # Dataset breakdown
    st.markdown("#### Dataset breakdown by category")
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    cat_counts["Avg price (₹)"] = cat_counts["Category"].map(
        df.groupby("category")["price"].mean().round(0).astype(int)
    )
    st.dataframe(cat_counts, hide_index=True, use_container_width=True)


# ── TAB 3: MODEL INSIGHTS ─────────────────────────────────────────────────────
with tab_insights:
    st.subheader("Model insights")
    st.caption("Understanding what the TF-IDF model has learned about your data.")

    vocab_size = len(vectorizer.vocabulary_)
    feature_names = vectorizer.get_feature_names_out()

    rows_html = f"""
    <div class="analytics-card" style="margin-bottom:1rem">
    <div class="insight-row"><span class="insight-key">Algorithm</span><span class="insight-val">TF-IDF + Cosine similarity</span></div>
    <div class="insight-row"><span class="insight-key">Fuzzy matching</span><span class="insight-val">rapidfuzz (Levenshtein)</span></div>
    <div class="insight-row"><span class="insight-key">N-gram range</span><span class="insight-val">(1, 2) — unigrams + bigrams</span></div>
    <div class="insight-row"><span class="insight-key">Vocabulary size</span><span class="insight-val">{vocab_size:,} terms</span></div>
    <div class="insight-row"><span class="insight-key">Documents indexed</span><span class="insight-val">{len(df):,}</span></div>
    <div class="insight-row"><span class="insight-key">sublinear_tf</span><span class="insight-val">True (log-dampened frequencies)</span></div>
    </div>
    """
    st.markdown(rows_html, unsafe_allow_html=True)

    # Top TF-IDF terms per category
    st.markdown("#### Top TF-IDF terms per category")
    import numpy as np
    for cat in sorted(df["category"].unique()):
        cat_df = df[df["category"] == cat]
        cat_matrix = vectorizer.transform(cat_df["search_text"])
        mean_scores = cat_matrix.mean(axis=0).A1
        top_idx = mean_scores.argsort()[::-1][:8]
        top_terms = ", ".join(feature_names[i] for i in top_idx)
        st.markdown(f"**{cat}** — `{top_terms}`")

    # Score distribution hint
    st.markdown("#### How similarity scores are distributed")
    st.markdown(
        "Scores range from 0 (no match) to 1 (perfect match). "
        "TF-IDF cosine scores are typically **0.1 – 0.6** for good matches. "
        "The default threshold of **0.15** balances recall vs precision. "
        "Use the sidebar slider to tune this for your query."
    )