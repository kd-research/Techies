import json, glob
import numpy as np
from pydantic import PrivateAttr
from ....predefined_tools.base_tool import BaseTool, BaseModel, Field, Type, List, os
from typing import Type, List, Any
from sentence_transformers import SentenceTransformer
import faiss

class QueryMechanicsToolSchema(BaseModel):
  query: str = Field(type=str, description="Search query for game mechanic.")
    
class QueryMechanicsTool(BaseTool):
  name: str = "Query Mechanics Tool"
  id: str = "query_mechanics"
  description: str = (
      "Searches a JSON file of game mechanics (with precomputed embeddings) for the closest "
      "semantic match to the query. Returns matching mechanics that fall within a given threshold."
      "Must have an embeddings file ending with '_embedded.json' in the current working directory."
  )
  args_schema: Type[BaseModel] = QueryMechanicsToolSchema

  _embeddings_file: str = PrivateAttr()
  _initial_top_k: int = PrivateAttr()
  _threshold: float = PrivateAttr()
  _mechanics: List[Any] = PrivateAttr()
  _embeddings: np.ndarray = PrivateAttr()
  _dimension: int = PrivateAttr()
  _index: Any = PrivateAttr()
  _model: Any = PrivateAttr()

  def __init__(self, initial_top_k: int = 15, threshold: float = 1.5, **kwargs):
      super().__init__(**kwargs)
      
      embedded_files = glob.glob(os.path.join(os.getcwd(), "*_embedded.json"))
      if embedded_files:
          # Use the first matching file in the working directory
          self._embeddings_file = os.path.normpath(embedded_files[0])
      else:
          # Fallback to the default path relative to __file__
          self._embeddings_file = os.path.normpath(
              print("No embedded files found in the current directory. Using default path for platformer mechanics."),
              os.path.join(os.path.dirname(__file__), "../refs/mechanics_db/platformer_mechanics_embedded.json")
          )      
          
      self._initial_top_k = initial_top_k
      self._threshold = threshold

      # Load the mechanics JSON with embeddings
      try:
          with open(self._embeddings_file, 'r') as infile:
              self._mechanics = json.load(infile)
      except Exception as e:
          raise ValueError(f"Failed to load mechanics from {self._embeddings_file}: {e}")

      # Build a FAISS index from the precomputed embeddings
      try:
          self._embeddings = np.array([m['embedding'] for m in self._mechanics]).astype('float32')
          self._dimension = self._embeddings.shape[1]
          self._index = faiss.IndexFlatL2(self._dimension)
          self._index.add(self._embeddings)
      except Exception as e:
          raise ValueError(f"Failed to build FAISS index: {e}")

      # Initialize the SentenceTransformer for query encoding
      try:
          self._model = SentenceTransformer('all-MiniLM-L6-v2')
      except Exception as e:
          raise ValueError(f"Failed to initialize SentenceTransformer: {e}")

  def _run(self, **kwargs) -> str:
      query = kwargs.get("query", "")
      if not query:
          return "No query provided."

      query_embedding = self._model.encode(query).astype('float32')
      query_embedding = np.expand_dims(query_embedding, axis=0)

      distances, indices = self._index.search(query_embedding, self._initial_top_k)

      relevant_results = []
      for dist, idx in zip(distances[0], indices[0]):
          if dist < self._threshold:
              normalized_similarity = max(0, (self._threshold - dist) / self._threshold)
              mechanic = self._mechanics[idx]
              mechanic['similarity_score'] = round(normalized_similarity, 4)
              relevant_results.append(mechanic)

      if not relevant_results:
          return "No relevant game mechanics found for your query."

      response_lines = []
      for i, result in enumerate(relevant_results, 1):
          response_lines.append(f"Result {i}:")
          response_lines.append(f"Name: {result.get('Name', 'N/A')}")
          response_lines.append(f"Description: {result.get('Description', 'N/A')}")
          response_lines.append(f"Implementation Details: {result.get('Implementation Details', 'N/A')}")
          response_lines.append(f"Pseudocode: {result.get('Pseudocode', 'N/A')}")
          response_lines.append(f"Similarity Score: {result.get('similarity_score', 'N/A')}\n")
      return "\n".join(response_lines)

  async def _arun(self, **kwargs) -> str:
      return self._run(**kwargs)
