import faiss
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def find_optimal_clusters(faiss_filepath):
    """Finds the optimal number of clusters for a given FAISS index using silhouette scores."""

    # Ensure the FAISS file exists at the provided file path
    if not os.path.exists(faiss_filepath):
        print(f"❌ Error: FAISS file '{faiss_filepath}' not found.")
        return None

    # Load FAISS index
    index = faiss.read_index(faiss_filepath)

    # Retrieve embeddings from FAISS
    embeddings = np.zeros((index.ntotal, index.d), dtype='float32')
    index.reconstruct_n(0, index.ntotal, embeddings)

    while True:
        # Prompt user for the range of cluster values
        try:
            min_k = int(input("Enter the minimum number of clusters to test: "))
            max_k = int(input("Enter the maximum number of clusters to test: "))
            if min_k < 2 or max_k <= min_k:
                raise ValueError
            if max_k > embeddings.shape[0]:  # max_k should not exceed the number of samples
                print(f"❌ The maximum number of clusters cannot be greater than {embeddings.shape[0]}.")
                continue
        except ValueError:
            print("❌ Invalid input. Please enter valid integer values where max_k > min_k ≥ 2.")
            continue

        silhouette_scores = []

        # Run K-means for different cluster sizes
        for k in range(min_k, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)
            silhouette_scores.append((k, score))
            print(f"✔️ Clusters: {k}, Silhouette Score: {score:.4f}")

        # Plot silhouette scores
        k_values, scores = zip(*silhouette_scores)
        plt.figure(figsize=(8, 5))
        plt.plot(k_values, scores, marker='o', linestyle='-', color='b')
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Silhouette Score")
        plt.title("Silhouette Score vs. Number of Clusters")
        plt.grid()
        plt.show()

        # Ask user if they want to rerun with a different range
        repeat = input("Do you want to try a different range? (yes/no): ").strip().lower()
        if repeat != "yes":
            break

    # Prompt user for the final number of clusters
    while True:
        try:
            optimal_k = int(input("Enter the optimal number of clusters: "))
            if optimal_k < min_k or optimal_k > max_k:
                raise ValueError
            break
        except ValueError:
            print(f"❌ Please enter a number between {min_k} and {max_k}.")

    print(f"✅ Optimal number of clusters selected: {optimal_k}")
    return optimal_k
