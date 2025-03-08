import os
import openai

def label_clusters_with_chatgpt(clusters_folder):
    with open('OpenAI_API_Key.txt', 'r') as file:
        openai_api_key = file.read().strip()

    openai.api_key = openai_api_key  # Set API key

    # Get the parent directory of the clusters folder
    parent_folder = os.path.dirname(clusters_folder)
    
    # Path to the cluster_labels.txt file (in the folder above 'clusters')
    cluster_labels_path = os.path.join(parent_folder, "cluster_labels.txt")
    
    # Initialize a list to hold the labels
    cluster_labels = []
    
    # Iterate through all .txt files in the clusters folder
    for file_name in sorted(os.listdir(clusters_folder), key=lambda x: int(x.split("_")[1].split("_")[0])):
        if file_name.endswith(".txt"):
            file_path = os.path.join(clusters_folder, file_name)
            
            # Read the content of the current cluster file
            with open(file_path, "r", encoding="utf-8") as f:
                cluster_content = f.read()
            
            # Construct the messages format
            messages = [
                {"role": "system", "content": "You generate exactly ONE concise four-word label for a set of topics."},
                {"role": "user", "content": f"Provide a single four-word label for these topics, with NO numbers or extra words:\n\n{cluster_content}"}
            ]
            
            # Call the OpenAI API using ChatCompletion
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0125",
                    messages=messages,
                    max_tokens=10,  # Ensuring short output
                    temperature=0.3  # Lower randomness for consistency
                )
                
                # Extract the label from the response
                label = response["choices"][0]["message"]["content"].strip()
                
                # Append the label to the list of cluster labels
                cluster_labels.append(label)
                
                print(f"✅ Labeled {file_name} as: {label}")
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # Save only the labels to 'cluster_labels.txt'
    with open(cluster_labels_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cluster_labels))
    
    print(f"✅ Saved all labels to {cluster_labels_path}")
