from embed_text import create_faiss_embedding
from kmeans_opt import find_optimal_clusters
from kmeans import perform_kmeans_clustering
from move_to_cluster import separate_clusters_by_request
import shutil
import os

def main():
    # Input file with data for creating the FAISS index
    file_name = "user_inputs_list.txt"

    # Create FAISS index from the input file
    faiss_filepath = create_faiss_embedding(file_name)

    # Extract the folder path of the FAISS file
    folder_path = os.path.dirname(faiss_filepath)

    #Define the destination path for the summarized_topics.txt
    summarized_topics_path = os.path.join(folder_path, "summarized_topics.txt")

    # Copy the original file to the new location with the new name
    shutil.copy(file_name, summarized_topics_path)
    
    # print(f"✅ FAISS index created at: {faiss_filepath}")

    optimal_clusters = find_optimal_clusters(faiss_filepath)
    
    perform_kmeans_clustering(faiss_filepath, optimal_clusters)
    separate_clusters_by_request(faiss_filepath)


if __name__ == "__main__":
    main()