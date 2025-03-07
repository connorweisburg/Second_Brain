import os
import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key-here'

def label_clusters_with_chatgpt(clusters_folder):
    # Get the parent directory of the clusters folder
    parent_folder = os.path.dirname(clusters_folder)
    
    # Path to the cluster_labels.txt file (in the folder above 'clusters')
    cluster_labels_path = os.path.join(parent_folder, "cluster_labels.txt")
    
    # Initialize a list to hold the labels
    cluster_labels = []
    
    # Iterate through all .txt files in the clusters folder
    for file_name in os.listdir(clusters_folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(clusters_folder, file_name)
            
            # Read the content of the current cluster file
            with open(file_path, "r", encoding="utf-8") as f:
                cluster_content = f.read()
            
            # Construct the prompt
            prompt = f"label these topics in 5 words:\n{cluster_content}"
            
            # Call the OpenAI API to generate a label for this cluster
            try:
                response = openai.Completion.create(
                    model="gpt-3.5-turbo",
                    prompt=prompt,
                    max_tokens=50,  # Adjust max_tokens if necessary
                    temperature=0.5  # You can adjust the temperature for randomness
                )
                
                # Extract the label from the response
                label = response.choices[0].text.strip()
                
                # Append the label to the list of cluster labels
                cluster_labels.append(f"{file_name}: {label}")
                
                print(f"✅ Labeled {file_name}")
            
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # Save the cluster labels to a new file 'cluster_labels.txt'
    with open(cluster_labels_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cluster_labels))
    
    print(f"✅ Saved all labels to {cluster_labels_path}")

