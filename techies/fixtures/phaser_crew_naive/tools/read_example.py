from techies.predefined_tools.base_tool import BaseTool, BaseModel, Type, os


class ReadExamplesToolSchema(BaseModel):
    pass

class ReadExamplesTool(BaseTool):
    name: str = "Read code examples"
    id: str = "read_examples"
    description: str = "Read the Phaser code examples."
    args_schema: Type[BaseModel] = ReadExamplesToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:
        with open(os.path.join(os.path.dirname(__file__), "template", "js", "common.js"), "r", encoding="utf-8") as f:
            common_js = f.read()
        with open(os.path.join(os.path.dirname(__file__), "template", "js", "main.js"), "r", encoding="utf-8") as f:
            examples = f.read()
        return common_js + examples
    

register_tool(ReadExamplesTool)