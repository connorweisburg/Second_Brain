import faiss
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import pandas as pd

# Load the FAISS index
index = faiss.read_index("user_interests_index.faiss")

# Number of clusters you want to create
num_clusters = 8  # You can adjust this as needed

# Retrieve embeddings from the FAISS index
embeddings = np.zeros((index.ntotal, index.d), dtype='float32')
index.reconstruct_n(0, index.ntotal, embeddings)

# Load user inputs for hover text
with open("summarized_user_requests.txt", "r", encoding="utf-8") as f:
    user_inputs = [line.strip() for line in f.readlines()]

# Run K-means clustering on the embeddings
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(embeddings)

# Get the cluster labels for each user input
labels = kmeans.labels_

# Perform PCA to reduce dimensionality to 3D for visualization
pca = PCA(n_components=3)
pca_embeddings = pca.fit_transform(embeddings)

# Create a DataFrame for visualization
df = pd.DataFrame(pca_embeddings, columns=['PCA1', 'PCA2', 'PCA3'])
df['Cluster'] = labels
df['User Input'] = user_inputs  # Adding user input for hover text

# Use Plotly to create an interactive 3D scatter plot
fig = px.scatter_3d(df, 
                    x='PCA1', 
                    y='PCA2', 
                    z='PCA3', 
                    color='Cluster', 
                    title="K-means Clustering (3D)", 
                    hover_data={'User Input': True, 'Cluster': True})

# Show the plot
fig.show()

# Optionally, save the cluster assignments to a file
with open("cluster_assignments.txt", "w", encoding="utf-8") as f:
    for i, label in enumerate(labels):
        f.write(f"User input {i+1}: Cluster {label}\n")

print(f"✅ K-means clustering completed with {num_clusters} clusters.")
