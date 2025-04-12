from .base_tool import BaseTool, BaseModel, Type, os


class ListFilesToolSchema(BaseModel):
    pass


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
            files = set([f for f in files if not f.startswith('.') and os.path.isfile(f"{self.base_dir}/{f}")])
            # blacklist
            files.discard("agentops.log")

            if not files:
                return "# -- Theres nothing to be listed -- #"
            return "\n".join(files)
        except Exception as e:
            return f"Failed to list files: {e}" 