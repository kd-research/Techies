from .base_tool import BaseTool, BaseModel, Field, Type, os, json


class WriteFileToolSchema(BaseModel):
    path: str = Field(type=str, description="The path to the file to write.")

    content: str = Field(
        type=str,
        description=
        "The content to write to the file. Field should be formatted as a string."
    )


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
            elif not os.path.exists(f"{self.base_dir}/{path}"):
                with open(f"{self.base_dir}/{path}", "w") as f:
                    f.write(content)
                return f"File {path} created successfully."
            else:
                with open(f"{self.base_dir}/{path}", "r") as f:
                    old_content = f.read()

                if path.endswith(".html") and (len(old_content.splitlines()) * 0.8 > len(content.splitlines())):
                    return f"""
Updating file {path} is rejected because new content is significantly smaller than the old content.
You should include every unchanged line in output html file. Also target this file to be run-as-is.
Please Try Again.
"""

                with open(f"{self.base_dir}/{path}", "w") as f:
                    f.write(content)

                diff = difflib.unified_diff(old_content.splitlines(), content.splitlines(), fromfile=f"before/{path}", tofile=f"after/{path}")
                diff = "\n".join(diff)
                return f"File {path} updated successfully.Summary of Changes:\n\n{diff}"

        except Exception as e:
            return f"Failed to write file: {e}" 