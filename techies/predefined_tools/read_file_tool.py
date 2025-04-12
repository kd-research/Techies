from .base_tool import BaseTool, BaseModel, Field, Type, os


class ReadFileToolSchema(BaseModel):
    path: str = Field(type=str, description="The path to the file to read.")


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