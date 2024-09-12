import json
import os
import re
import requests

from bs4 import BeautifulSoup
from crewai_tools import BaseTool
from freesound import FreesoundClient
from pydantic.v1 import BaseModel, Field
from tempfile import TemporaryDirectory
from typing import Type, List, Dict, Any, Optional


class ReadFileToolSchema(BaseModel):
    path: str = Field(type=str, description="The path to the file to read.")


class BatchReadFilesToolSchema(BaseModel):
    paths: List[str] = Field(
        type=List[str], description="An array of filenames to read."
    )


class WriteFileToolSchema(BaseModel):
    path: str = Field(type=str, description="The path to the file to write.")

    content: str = Field(
        type=str,
        description=
        "The content to write to the file. Field should be formatted as a string."
    )


class ListFilesToolSchema(BaseModel):
    pass


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

class ReadHtmlExamplesToolSchema(BaseModel):
    pass

class ReadFileTool(BaseTool):
    name: str = "Read a File"
    id: str = "read_file"
    description: str = "Read the contents of a file from the bucket."
    args_schema: Type[BaseModel] = ReadFileToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        try:
            path = kwargs['path']
            with open(f"{self.base_dir}/{path}", "r") as f:
                content = f.read()

            return content
        except Exception as e:
            files_available = "\t".join(os.listdir(self.base_dir))
            return f"Failed to read file: {e}.\nFiles available: {files_available}"


class BatchReadFilesTool(BaseTool):
    name: str = "Read Some Files"
    id: str = "batch_read_files"
    description: str = "Read contents of files. Same as read_file but for multiple files."
    args_schema: Type[BaseModel] = BatchReadFilesToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        try:
            paths = kwargs['paths']
            content = ""
            for path in paths:
                with open(f"{self.base_dir}/{path}", "r") as f:
                    content += f.read()
                    content += "\n"

            return content
        except Exception as e:
            return f"Failed to read files: {e}"


class WriteFileTool(BaseTool):
    name: str = "Update a File"
    id: str = "write_file"
    description: str = "Write content of a file to the bucket."
    args_schema: Type[BaseModel] = WriteFileToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        try:
            import difflib

            path = kwargs['path'].replace("/", "-")
            content = kwargs['content']

            if not isinstance(content, str):
                content = json.dumps(content)

            if not os.path.exists(self.base_dir):
                with open(f"{self.base_dir}/{path}", "w") as f:
                    f.write(content)

                return f"File {path} created successfully."
            else:
                with open(f"{self.base_dir}/{path}", "r") as f:
                    old_content = f.read()

                with open(f"{self.base_dir}/{path}", "w") as f:
                    f.write(content)

                diff = difflib.unified_diff(old_content.splitlines(), content.splitlines(), fromfile=f"before/{path}", tofile=f"after/{path}")
                diff = "\n".join(diff)
                return f"File {path} updated successfully.Summary of Changes:\n\n{diff}"

        except Exception as e:
            return f"Failed to write file: {e}"


class ListFilesTool(BaseTool):
    name: str = "List Existing Files"
    id: str = "list_files"
    description: str = "List the files in current bucket."
    args_schema: Type[BaseModel] = ListFilesToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        try:
            files = os.listdir(self.base_dir)
            files = [f for f in files if not f.startswith('.') and os.path.isfile(f"{self.base_dir}/{f}")]
            if not files:
                return "# -- Theres nothing to be listed -- #"
            return "\n".join(files)
        except Exception as e:
            return f"Failed to list files: {e}"


class SearchSoundTool(BaseTool):
    name: str = "search_sound"
    id: str = "search_sound"
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
    description: str = "Save a sound file from FreeSound using the sound ID."
    args_schema: Type[BaseModel] = SaveSoundToolSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        sound_id = kwargs['sound_id']
        file_name = kwargs['file_name']

        client = FreesoundClient()
        client.set_token(os.environ['FREESOUND_CLIENT_API_KEY'], 'token')

        current_directory = os.getcwd()
        try:
            chosen_sound = client.get_sound(sound_id)
            chosen_sound.retrieve_preview(current_directory, file_name)
            return f"Sound with id: {sound_id}, with name: {file_name}."
        except Exception as e:
            return f"Failed to save sound: {e}"

class ReadHtmlExamplesTool(BaseTool):
    name: str = "Read HTML examples"
    id: str = "read_examples_html"
    description: str = "Read all example html games."
    args_schema: Type[BaseModel] = ReadHtmlExamplesToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> Dict[str, Dict[str, str]]:
        examples_dir = os.path.normpath(__file__ + '/../refs/html_game_examples')
        examples = {}

        try:
            for filename in os.listdir(examples_dir):
                file_path = os.path.join(examples_dir, filename)
                if filename.endswith('.html'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        examples[filename] = f.read()

            return examples
        except Exception as e:
            return f"Failed to read examples: {e}"

def get_all_tools():
    # base_dir = TemporaryDirectory(delete=False).name
    base_dir = "."

    # print(f"Temp directory created at: {base_dir}")

    def no_cache(args, result):
        return False

    tools = {}
    toolklasses = [
        ReadFileTool, BatchReadFilesTool, WriteFileTool, ListFilesTool,
        SaveSoundTool, SearchSoundTool, ReadHtmlExamplesTool
    ]
    for toolkls in toolklasses:
        tool = toolkls(base_dir=base_dir)
        tool.cache_function = no_cache
        tools[tool.id] = tool

    return tools
