import numpy as np
import faiss
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load FAISS index
index = faiss.read_index("user_interests_index.faiss")

# Extract embeddings from the FAISS index
embeddings = np.array([index.reconstruct(i) for i in range(index.ntotal)]).astype("float32")

# Range of k values to test (number of clusters)
k_range = range(2, 11)

# Calculate inertia for each k
sil_scores = []
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    cluster_labels = kmeans.fit_predict(embeddings)
    score = silhouette_score(embeddings, cluster_labels)
    sil_scores.append(score)

# Plot Silhouette scores
plt.figure(figsize=(8, 6))
plt.plot(k_range, sil_scores, marker='o')
plt.title("Silhouette Scores for Different Numbers of Clusters")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Silhouette Score")
plt.grid(True)
plt.show()
