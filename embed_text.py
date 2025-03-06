import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def create_faiss_embedding(txt_filename):
    """Embeds text from a given .txt file and saves the FAISS index in a new folder."""
    
    # Remove the .txt extension for folder & filenames
    base_name = txt_filename.replace(".txt", "")

    # Create a folder with the same name as the file (without .txt)
    output_folder = base_name  # This is the folder where the FAISS file will be stored
    os.makedirs(output_folder, exist_ok=True)

    # Define FAISS output file path (ensure no extra subfolder)
    faiss_filepath = os.path.join(output_folder, f"{base_name}.faiss")

    # Load user inputs from file
    try:
        with open(txt_filename, "r", encoding="utf-8") as f:
            user_inputs = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"❌ Error: File '{txt_filename}' not found.")
        return None  # Return None so app.py can handle the error properly

    # ✅ Load embedding model **only once per function call**
    print("⏳ Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded!")

    # Convert each input into an embedding
    embeddings = np.array([model.encode(text, normalize_embeddings=True) for text in user_inputs]).astype("float32")

    # Create FAISS index and store embeddings
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save FAISS index in the new folder
    faiss.write_index(index, faiss_filepath)

    print(f"✅ Embedded {len(user_inputs)} user inputs and saved FAISS index in '{output_folder}/'")
    print(f"   - FAISS file: {faiss_filepath}")

    return faiss_filepath  # ✅ Return the FAISS file path
