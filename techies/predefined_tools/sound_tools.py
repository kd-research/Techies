from .base_tool import BaseTool, BaseModel, Field, Type, List, Dict, Any, os, requests, re
from bs4 import BeautifulSoup
from freesound import FreesoundClient


class SearchSoundToolSchema(BaseModel):
    query: str = Field(type=str, description="Search query for the sound.")
    min_duration: int = Field(
        type=int, description="Minimum duration of the sound in seconds."
    )
    max_duration: int = Field(
        type=int, description="Maximum duration of the sound in seconds."
    )
    max_results: int = Field(
        default=8,
        type=int,
        description="Maximum number of search results to return."
    )


class SaveSoundToolSchema(BaseModel):
    sound_id: int = Field(type=int, description="ID of the sound to save.")
    file_name: str = Field(
        type=str, description="Name of the saved sound file."
    )


class SearchSoundTool(BaseTool):
    name: str = "search_sound"
    id: str = "search_sound"
    base_dir: str = "." # Not used in this tool, mute error when base_dir is assigned
    description: str = "Search for sounds using the FreeSound API."
    args_schema: Type[BaseModel] = SearchSoundToolSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> List[Dict[str, Any]]:
        query = kwargs['query']
        min_duration = kwargs['min_duration']
        max_duration = kwargs['max_duration']
        max_results = kwargs.get('max_results', 8)

        client = FreesoundClient()
        client.set_token(os.environ.get('FREESOUND_CLIENT_API_KEY'), 'token')
        results = client.text_search(
            query=query, filter=f"duration:[{min_duration} TO {max_duration}]"
        )

        fetched_results = []
        for idx, sound in enumerate(results):
            if idx >= max_results:
                break

            sound_id = sound.id
            sound_user = sound.username
            sound_url = f"https://freesound.org/people/{sound_user}/sounds/{sound_id}/"

            page = requests.get(sound_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            sound_description = soup.find(id="soundDescriptionSection")
            sound_description = re.sub(r'<.*?>', '', str(sound_description))

            fetched_results.append(
                {
                    "sound": sound,
                    "name": sound.name,
                    "description": sound_description,
                }
            )

        return fetched_results


class SaveSoundTool(BaseTool):
    name: str = "save_sound"
    id: str = "save_sound"
    base_dir: str
    description: str = "Save a sound file from FreeSound using the sound ID."
    args_schema: Type[BaseModel] = SaveSoundToolSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        sound_id = kwargs['sound_id']
        file_name = kwargs['file_name']

        client = FreesoundClient()
        client.set_token(os.environ['FREESOUND_CLIENT_API_KEY'], 'token')

        sounds_dir = os.path.join(self.base_dir, "sounds")
        os.makedirs(sounds_dir, exist_ok=True)

        try:
            chosen_sound = client.get_sound(sound_id)
            chosen_sound.retrieve_preview(sounds_dir, file_name)
            return f"Sound with id: {sound_id}, with name: {file_name} saved in {sounds_dir}."
        except Exception as e:
            return f"Failed to save sound: {e}" 