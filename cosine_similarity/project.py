import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz

# Configuration
SIMILARITY_THRESHOLD = 0.15
TOP_K_RESULTS = 10
FUZZY_MATCH_COUNT = 5
FUZZY_CUTOFF = 0.3

@st.cache_resource
def load_model():
    """Load and cache the vectorizer and TF-IDF matrix."""
    df = pd.read_csv("real product.csv")
    
    # Handle missing values
    df["product_name"] = df["product_name"].fillna("").astype(str)
    df["category"] = df["category"].fillna("").astype(str)
    
    # Create search text with additional fields if available
    df["search_text"] = df["product_name"].str.lower() + " " + df["category"].str.lower()
    if "brand" in df.columns:
        df["search_text"] = df["search_text"] + " " + df["brand"].fillna("").str.lower()
    if "description" in df.columns:
        df["search_text"] = df["search_text"] + " " + df["description"].fillna("").str.lower()
    
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df["search_text"])
    
    return df, vectorizer, tfidf_matrix

def search_products(query, df, vectorizer, tfidf_matrix, threshold=SIMILARITY_THRESHOLD):
    """Search products using fuzzy matching and cosine similarity."""
    # Empty string guard
    if not query or not query.strip():
        return pd.DataFrame()
    
    query = query.lower().strip()
    
    # Use rapidfuzz for fuzzy matching (10x faster than difflib)
    all_text = df["search_text"].tolist()
    fuzzy_results = process.extract(query, all_text, scorer=fuzz.partial_ratio, limit=FUZZY_MATCH_COUNT)
    close_matches = [match[0] for match in fuzzy_results if match[1] / 100 >= FUZZY_CUTOFF]
    
    search_queries = [query] + close_matches
    
    query_vector = vectorizer.transform(search_queries)
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)
    
    final_scores = similarity_scores.max(axis=0)
    
    # Use df.copy() to avoid modifying original dataframe
    results = df.copy()
    results["similarity"] = final_scores
    
    results = results[results["similarity"] > threshold]
    results = results.sort_values(by="similarity", ascending=False)
    
    return results.head(TOP_K_RESULTS)

# Load cached model
df, vectorizer, tfidf_matrix = load_model()

st.title("Smart Product Search Engine")
st.markdown("🔍 *AI-powered semantic search with fuzzy matching*")

query = st.text_input("Enter product name, category, or description", placeholder="e.g., wireless headphones")

if st.button("Search") or query:
    with st.spinner("Searching..."):
        results = search_products(query, df, vectorizer, tfidf_matrix)

    if results.empty:
        st.warning("No products found. Try a different search term.")
    else:
        st.subheader(f"Found {len(results)} results")
        
        # Determine columns to display based on available data
        display_cols = ["product_name", "category", "price", "similarity"]
        optional_cols = ["brand", "rating", "review_count"]
        
        for col in optional_cols:
            if col in results.columns:
                display_cols.insert(-1, col)
        
        # Format similarity as percentage
        results_display = results.copy()
        results_display["similarity"] = results_display["similarity"].apply(lambda x: f"{x*100:.1f}%")
        
        st.dataframe(results_display[display_cols], use_container_width=True)
        
        # Show top match details if description available
        if "description" in results.columns and not results.empty:
            with st.expander("View Top Match Details"):
                top_match = results.iloc[0]
                st.write(f"**{top_match['product_name']}**")
                if "description" in top_match and pd.notna(top_match['description']):
                    st.write(top_match['description'])
                if "image_url" in top_match and pd.notna(top_match['image_url']):
                    st.image(top_match['image_url'], width=200)