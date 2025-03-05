import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model (lightweight & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load user inputs from file
with open("user_interests_with_timestamps.txt", "r", encoding="utf-8") as f:
    user_inputs = [line.strip().split(" | ", 1)[1] for line in f.readlines()]

# Convert each input into an embedding
embeddings = np.array([model.encode(text, normalize_embeddings=True) for text in user_inputs]).astype("float32")

# Create FAISS index and store embeddings
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save FAISS index & user inputs
faiss.write_index(index, "user_interests_index.faiss")

with open("user_inputs_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(user_inputs))

print(f"✅ Embedded {len(user_inputs)} user inputs and stored in FAISS!")
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model (lightweight & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load user inputs from file
with open("user_interests_with_timestamps.txt", "r", encoding="utf-8") as f:
    user_inputs = [line.strip().split(" | ", 1)[1] for line in f.readlines()]

# Convert each input into an embedding
embeddings = np.array([model.encode(text, normalize_embeddings=True) for text in user_inputs]).astype("float32")

# Create FAISS index and store embeddings
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save FAISS index & user inputs
faiss.write_index(index, "user_interests_index.faiss")

with open("user_inputs_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(user_inputs))

print(f"✅ Embedded {len(user_inputs)} user inputs and stored in FAISS!")
