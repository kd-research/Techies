from techies.predefined_tools.base_tool import BaseTool, BaseModel, Type, Field
import os
import base64
from openai import OpenAI

class IconToolSchema(BaseModel):
    icon_description: str = Field(
        type=str,
        description="Description of the icon image to generate."
    )


class IconTool(BaseTool):
    name: str = "Icon generator"
    id: str = "icon_gen"
    description: str = "Create icon images for a game app."
    args_schema: Type[BaseModel] = IconToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, icon_description: str) -> str:
        client: OpenAI = OpenAI()

        # make external directory if not exists
        os.makedirs(os.path.join(self.base_dir, "external"), exist_ok=True)
        icon_path = os.path.join(self.base_dir, "external", "icon.png")

        # Generate icon image
        icon_img = client.images.generate(
            model="dall-e-3",
            prompt="Create a game app icon image for the description:\n"+icon_description+"\nUse transparent background",
            n=1,
            size="1024x1024"
        )
        image_bytes = base64.b64decode(icon_img.data[0].b64_json)
        with open(icon_path, "wb") as f:
            f.write(image_bytes)

        return f"Icon image generated successfully."
    
    
register_tool(IconTool)