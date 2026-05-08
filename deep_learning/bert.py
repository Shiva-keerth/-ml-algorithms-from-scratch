import pandas as pd
import numpy as np
import re


from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


# Load data
df = pd.read_csv("product_recommendation_dataset.csv")


TEXT_COLUMNS = 'description'
NAME_COLUMN = 'product_name'


# ✅ Better cleaning (keep spaces)
def clean_text(text):
   text = str(text).lower()
   text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
   return text.strip()


df["clean_text"] = df[TEXT_COLUMNS].apply(clean_text)


# Load model
bert_model = SentenceTransformer("all-MiniLM-L6-v2")


# Normalize embeddings (important)
bert_embeddings = bert_model.encode(
   df["clean_text"].tolist(),
   show_progress_bar=True,
   normalize_embeddings=True
)


# Recommendation function
def recommend_bert(product_name, top_n=5):
   if product_name not in df[NAME_COLUMN].values:
       return "Product not found"


   idx = df[df[NAME_COLUMN] == product_name].index[0]


   scores = cosine_similarity(
       [bert_embeddings[idx]],
       bert_embeddings
   )[0]


   # Sort highest similarity first
   top_indices = scores.argsort()[::-1][1:top_n+1]


   return df[NAME_COLUMN].iloc[top_indices].tolist()


# Search function
def search_text(query, top_n=5):
   query = clean_text(query)


   query_embedding = bert_model.encode(
       [query],
       normalize_embeddings=True
   )


   scores = cosine_similarity(query_embedding, bert_embeddings)[0]


   # FIX: reverse sorting
   top_indices = scores.argsort()[::-1][:top_n]


   return df.iloc[top_indices][[NAME_COLUMN, TEXT_COLUMNS]]


# Search + Recommend
def search_and_recommend(query, top_n=5):
   query = clean_text(query)


   query_embedding = bert_model.encode(
       [query],
       normalize_embeddings=True
   )


   scores = cosine_similarity(query_embedding, bert_embeddings)[0]


   best_idx = scores.argmax()
   best_product = df.iloc[best_idx][NAME_COLUMN]


   recommendation = recommend_bert(best_product, top_n)


   return {
       "searched_product": best_product,
       "recommendation": recommendation
   }


# CLI loop
print("System ready (Type 'exit' to stop)")


while True:
   user_query = input("\nEnter product to search: ")


   if user_query.lower() == "exit":
       print("Exiting...")
       break


   print("\nTop Matches:")
   print(search_text(user_query))


   result = search_and_recommend(user_query)


   print("\nBest Match:", result["searched_product"])
   print("Recommendations:", result["recommendation"])
   print("\n" + "="*50)
