from .base_tool import BaseTool, BaseModel, Field, Type, List, os


class BatchReadFilesToolSchema(BaseModel):
    paths: List[str] = Field(
        type=List[str], description="An array of filenames to read."
    )


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