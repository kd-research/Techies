from .base_tool import BaseTool, BaseModel, Type, Dict, os


class ReadHtmlExamplesToolSchema(BaseModel):
    pass


class ReadHtmlExamplesTool(BaseTool):
    name: str = "Read HTML examples"
    id: str = "read_examples_html"
    description: str = "Read all example html games."
    args_schema: Type[BaseModel] = ReadHtmlExamplesToolSchema
    base_dir: str = "." # Not used in this tool, mute error when base_dir is assigned

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> Dict[str, Dict[str, str]]:
        examples_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../refs/html_game_examples'))
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