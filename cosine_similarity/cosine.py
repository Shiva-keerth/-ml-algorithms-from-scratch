import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

a=np.array([1,2,3]).reshape(1,-1)
b=np.array([4,5,6]).reshape(1,-1)

similarity =cosine_similarity(a,b)
print("Similarity:",similarity[0][0])


dot_product=np.dot(a,b.T)
norm_a=np.linalg.norm(a)
norm_b=np.linalg.norm(b)

s=dot_product/(norm_a*norm_b)
print(s[0][0])