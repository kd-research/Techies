from techies.predefined_tools.base_tool import BaseTool, BaseModel, Type, os


class PackGameToolSchema(BaseModel):
    pass

FILE = __file__
class PackGameTool(BaseTool):
    name: str = "Pack game"
    id: str = "pack_game"
    description: str = "Pack the Phaser code into a game."
    args_schema: Type[BaseModel] = PackGameToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, **kwargs) -> str:

        try:
            with open(os.path.join(self.base_dir, "game.js"), "r", encoding="utf-8") as f:
                game_code = f.read()
            with open(os.path.join(os.path.dirname(FILE), "template", "js", "main.js"), "r", encoding="utf-8") as f:
                js_file = f.read()
            with open(os.path.join(os.path.dirname(FILE), "template", "index_template.html"), "r", encoding="utf-8") as f:
                html_file = f.read()
        except Exception as e:
            return f"Error reading game template: {e}"
        
        try:
            # append game_code to js_file
            js_file = js_file + "\n" + game_code

            # replace MainScene with CustomScene
            html_file = html_file.replace("MainScene", "CustomScene")

            # replace <script src="./js/main.js"></script> into <script> the js_file code </script>
            html_file = html_file.replace('<script src="./js/main.js"></script>', f'<script>{js_file}</script>')

            # write the html_file to index.html
            with open(f"{self.base_dir}/index.html", "w", encoding="utf-8") as f:
                f.write(html_file)

        except Exception as e:
            return f"Error packing game: {e}"
        

        # copy assets folder to base_dir
        assets_dir = os.path.join(self.base_dir, "assets")
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)
        for item in os.listdir(os.path.join(os.path.dirname(__file__), "template", "assets")):
            s = os.path.join(os.path.dirname(__file__), "template", "assets", item)
            d = os.path.join(assets_dir, item)
            if os.path.isdir(s):
                os.makedirs(d, exist_ok=True)
            else:
                with open(s, "rb") as fsrc, open(d, "wb") as fdst:
                    fdst.write(fsrc.read())
        

        return "Game packed successfully."


register_tool(PackGameTool)