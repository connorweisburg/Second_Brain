import os

def separate_clusters_by_request(file_path):
    """Organizes user inputs into clusters and saves separate files for each cluster."""
    
    # Extract folder path from the input file path
    folder_path = os.path.dirname(file_path)
    
    # Read the cluster assignments
    cluster_assignments = {}
    with open(os.path.join(folder_path, "cluster_assignments.txt"), "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(":")
            user_input_idx = int(parts[0].split()[2]) - 1  # Get the user input index (1-based to 0-based)
            cluster_label = int(parts[1].split()[1])  # Get the cluster number
            cluster_assignments[user_input_idx] = cluster_label
    
    # Read the summarized user requests
    with open(os.path.join(folder_path, "summarized_topics.txt"), "r", encoding="utf-8") as f:
        user_inputs = [line.strip() for line in f.readlines()]
    
    # Create a dictionary to store requests for each cluster
    clustered_requests = {}
    
    # Organize the user inputs into their respective clusters
    for idx, cluster_label in cluster_assignments.items():
        if cluster_label not in clustered_requests:
            clustered_requests[cluster_label] = []
        clustered_requests[cluster_label].append(user_inputs[idx])
    
    # Write the separated files for each cluster
    for cluster_label, requests in clustered_requests.items():
        filename = os.path.join(folder_path, f"cluster_{cluster_label}_requests.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(requests))
        
        print(f"✅ Saved cluster {cluster_label} requests to {filename}")
