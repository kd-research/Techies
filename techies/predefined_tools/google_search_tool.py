from pydantic import ConfigDict
from .base_tool import BaseTool, BaseModel, Field, Type
from langchain_community.utilities import GoogleSerperAPIWrapper

class GoogleSearchToolSchema(BaseModel):
    query: str = Field(type=str, description="The search query to use for Google search.")

class GoogleSearchTool(BaseTool):
    name: str = "Google Search"
    id: str = "google_search"
    description: str = "Search Google for recent results using the provided query."
    args_schema: Type[BaseModel] = GoogleSearchToolSchema

    search: GoogleSerperAPIWrapper = Field(default=None)  # Define search as a Pydantic field

    # Add model configuration for Pydantic
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, 'search', GoogleSerperAPIWrapper())  # Bypass Pydantic validation

    # Define the _run method to execute the search
    def _run(self, **kwargs) -> str:
        try:
            query = kwargs['query']
            results = self.search.run(query)
            return results
        except Exception as e:
            return f"Failed to perform Google search: {e}"