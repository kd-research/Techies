# import json
# import os
# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer
from techies.callbacks import register_callback

# Create embeddings file, used as callback for after mechanics.json is created by mechanicsgencrew
# to create embeddings for each mechanic and save them to a new JSON file. These mechanics can be
# searched using the query_mechanics tool.
def embed_json() -> None:
    """
    This function searches for a mechanics.json (required) file in the current directory and its subdirectories,
    computes embeddings for each mechanic using a BERT-based model, and saves the updated mechanics
    with embeddings to a new JSON file.
    """
    import json
    import os
    from sentence_transformers import SentenceTransformer
    mechanics_suffix = 'mechanics.json'
    current_directory = os.getcwd() 
    filename = None
    
    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.endswith(mechanics_suffix):
                filename = os.path.join(root, file)
                break
        if filename:
            break
    if filename:
        print(f"Mechanics file found: {filename}")
    else:
        print("No file ending in mechanics.json found. Exiting...")
        return
    
    with open(filename, 'r') as infile:
        mechanics = json.load(infile)

    # Initialize BERT-based model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Compute embedding for each mechanic and add it as a new field
    for mechanic in mechanics:
        text = f"{mechanic['Name']}. {mechanic['Description']}"
        embedding = model.encode(text).tolist()  # Convert numpy array to list for JSON serialization
        mechanic['embedding'] = embedding

    base_name, ext = os.path.splitext(filename)
    output_filename = f"{base_name}_embedded{ext}"

    with open(output_filename, 'w') as outfile:
        json.dump(mechanics, outfile, indent=2)

    print(f"Embeddings created and saved to '{output_filename}'.")
    
    
# Query mechanics
def search_mechanics_dynamic(query, initial_top_k=10, threshold=1.5):
    import faiss
    import numpy as np
    import os, json
    from sentence_transformers import SentenceTransformer


    embed_suffix = '_embedded.json'
    current_directory = os.getcwd() 
    filename = None
    mechanics = None
    for root, _, files in os.walk(current_directory):
        for file in files:
            if file.endswith(embed_suffix):
                filename = os.path.join(root, file)
                break
        if filename:
            break
    if not filename:
        print("No file ending in _embedded.json found. Exiting...")
        return
    
    with open(filename, 'r') as infile:
        mechanics = json.load(infile)
    
    embeddings = np.array([m['embedding'] for m in mechanics]).astype('float32')

    # Create a FAISS index (using L2 distance)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)  # Add our vectors to the index

    # Initialize the same SentenceTransformer model for queries
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Compute the query embedding using the same model
    query_embedding = model.encode(query).astype('float32')
    query_embedding = np.expand_dims(query_embedding, axis=0)
    
    # Retrieve a larger set of candidates initially
    distances, indices = index.search(query_embedding, initial_top_k)
    
    # lower distance means more similar.
    relevant_results = []
    for dist, idx in zip(distances[0], indices[0]):
        if dist < threshold:
            normalized_similarity = max(0, (threshold - dist) / threshold)
            mechanic = mechanics[idx]
            mechanic['similarity_score'] = round(normalized_similarity, 4)
            relevant_results.append(mechanic)
    return relevant_results

# def main():
#     # Uncomment the following line to create embeddings
#     embed_json()
    
#     # Uncomment the following lines to search for mechanics
#     query = input("Enter your query: ")
#     results = search_mechanics_dynamic(query, initial_top_k=15, threshold=1.4)
#     if results:
#         for idx, result in enumerate(results, 1):
#             print(f"Result {idx}:")
#             print("Name:", result["Name"])
#             print("Description:", result["Description"])
#             print("Implementation Details:", result["Implementation Considerations"])
#             print("Pseudocode:", result["Pseudocode"])
#             print("Similarity Score:", result["similarity_score"])
#             print("-")
#     else:
#         print("No relevant mechanics found for your query.")    
        

# if __name__ == "__main__":
#     main()

register_callback("embed_json", embed_json)