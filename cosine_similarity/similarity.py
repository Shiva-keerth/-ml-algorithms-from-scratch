from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sentences =["I Love Machine Learning",
            "I Love Artificial Learning"]

vectorizer =CountVectorizer()
vectors = vectorizer.fit_transform(sentences)

similarity=cosine_similarity(vectors)

print("cosine similarity")
print(similarity)
print(similarity[0][1])