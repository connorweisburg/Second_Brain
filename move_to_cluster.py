# Read the cluster assignments
cluster_assignments = {}
with open("cluster_assignments.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(":")
        user_input_idx = int(parts[0].split()[2]) - 1  # Get the user input index (1-based to 0-based)
        cluster_label = int(parts[1].split()[1])  # Get the cluster number
        cluster_assignments[user_input_idx] = cluster_label

# Read the summarized user requests
with open("summarized_user_requests.txt", "r", encoding="utf-8") as f:
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
    filename = f"cluster_{cluster_label}_requests.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(requests))

    print(f"✅ Saved cluster {cluster_label} requests to {filename}")
