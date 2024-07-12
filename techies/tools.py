import os
import json
from tempfile import TemporaryDirectory
from typing import Type, List, Dict, Any, Optional

from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool

class ReadFileToolSchema(BaseModel):
    path: str = Field(
        type=str,
        description="The path to the file to read"
    )

class BatchReadFilesToolSchema(BaseModel):
    paths: List[str] = Field(
        type=List[str],
        description="An array of paths to the files to read"
    )

class WriteFileToolSchema(BaseModel):
    path: str = Field(
        type=str,
        description="The path to the file to read"
    )

    content: Any = Field(
        type=Any,
        description="The content to write to the file"
    )

class ListFilesToolSchema(BaseModel):
    args: Optional[Dict[str, Any]] = Field(
        type=Optional[Dict[str, Any]],
        description="Additional arguments"
    )


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
            files_available = "\t".join(os.listdir(self.base_dir))
            return f"Failed to read file: {e}.\nFiles available: {files_available}"

class BatchReadFilesTool(BaseTool):
    name: str = "batch_read_files"
    description: str = "Read and concat the contents of multiple files in a batch"
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

            if not isinstance(content, str):
                content = json.dumps(content)

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
    toolklasses = [
        ReadFileTool, 
        BatchReadFilesTool,
        WriteFileTool, 
        ListFilesTool
    ]
    for toolkls in toolklasses:
        tool = toolkls(base_dir=base_dir)
        tools[tool.name] = tool

    return tools
