import os
import faiss
import numpy as np
from sklearn.cluster import KMeans

def perform_kmeans_clustering(faiss_filepath, num_clusters):
    """Performs K-means clustering on the FAISS embeddings and saves the output files in the same folder."""
    
    # Extract folder path from the FAISS file path
    folder_path = os.path.dirname(faiss_filepath)
    
    # Load the FAISS index
    index = faiss.read_index(faiss_filepath)
    
    # Retrieve embeddings from the FAISS index
    embeddings = np.zeros((index.ntotal, index.d), dtype='float32')
    index.reconstruct_n(0, index.ntotal, embeddings)
    
    # Run K-means clustering on the embeddings
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(embeddings)
    
    # Get the cluster labels for each data point
    labels = kmeans.labels_
    
    # Optionally, save the cluster assignments to a file
    cluster_assignments_file = os.path.join(folder_path, "cluster_assignments.txt")
    with open(cluster_assignments_file, "w", encoding="utf-8") as f:
        for i, label in enumerate(labels):
            f.write(f"Data point {i+1}: Cluster {label}\n")
    
    print(f"✅ Cluster assignments saved to {cluster_assignments_file}")
