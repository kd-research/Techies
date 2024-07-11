import os
from tempfile import TemporaryDirectory
from typing import Type

from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool

class ReadFileToolSchema(BaseModel):
    path: str = Field(
        type=str,
        description="The path to the file to read"
    )

class WriteFileToolSchema(BaseModel):
    path: str = Field(
        type=str,
        description="The path to the file to read"
    )

    content: str = Field(
        type=str,
        description="The content to write to the file"
    )

class ListFilesToolSchema(BaseModel):
    pass


class ReadFileTool(BaseTool):
    name: str = "read_file"
    description: str = "Read the contents of a file from the bucket"
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
            return f"Failed to read file: {e}"

class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = "Write content of a file to the bucket"
    args_schema: Type[BaseModel] = WriteFileToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        try:
            path = kwargs['path'].replace("/", "-")
            content = kwargs['content']
            with open(f"{self.base_dir}/{path}", "w") as f:
                f.write(content)

            return "File written successfully"
        except Exception as e:
            return f"Failed to write file: {e}"

class ListFilesTool(BaseTool):
    name: str = "list_files"
    description: str = "List the files in current bucket"
    args_schema: Type[BaseModel] = ListFilesToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        try:
            files = os.listdir(self.base_dir)
            return "\n".join(files)
        except Exception as e:
            return f"Failed to list files: {e}"

def get_all_tools():
    base_dir = TemporaryDirectory(delete=False).name
    print(f"Temp directory created at: {base_dir}")

    tools = {}
    for toolkls in [ReadFileTool, WriteFileTool, ListFilesTool]:
        tool = toolkls(base_dir=base_dir)
        tools[tool.name] = tool

    return tools
