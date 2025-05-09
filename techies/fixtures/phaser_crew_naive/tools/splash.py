from techies.predefined_tools.base_tool import BaseTool, BaseModel, Type, Field
import os
import base64
from openai import OpenAI

class SplashAndIconToolSchema(BaseModel):
    splash_description: str = Field(
        type=str,
        description="Description of the splash screen image to generate."
    )
    icon_description: str = Field(
        type=str,
        description="Description of the icon image to generate."
    )


class SplashAndIconTool(BaseTool):
    name: str = "Splash screen and icon generator"
    id: str = "splash_and_icon"
    description: str = "Create splash screen and icon images for a game app."
    args_schema: Type[BaseModel] = SplashAndIconToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI()

    def _run(self, **kwargs) -> str:

        splash_description = kwargs['splash_description']
        icon_description = kwargs['icon_description']

        # make external directory if not exists
        os.makedirs(os.path.join(self.base_dir, "external"), exist_ok=True)
        icon_path = os.path.join(self.base_dir, "external", "icon.png")
        splash_path = os.path.join(self.base_dir, "external", "splash.png")

        # Generate icon image
        icon_img = self.client.images.generate(
            model="gpt-image-1",
            prompt="Create a game app icon image for the description:\n"+icon_description+"\nUse transparent background",
            n=1,
            size="1024x1024"
        )
        image_bytes = base64.b64decode(icon_img.data[0].b64_json)
        with open(icon_path, "wb") as f:
            f.write(image_bytes)

        # Generate splash screen image
        splash_img = self.client.images.generate(
            model="dall-e-3",
            prompt="Create a game app splash screen image for the description:\n"+splash_description+"\nUse transparent background",
            n=1,
            size="1024x1024"
        )
        image_bytes = base64.b64decode(splash_img.data[0].b64_json)
        with open(splash_path, "wb") as f:
            f.write(image_bytes)
        return f"Icon and splash screen images generated successfully."
    

register_tool(SplashAndIconTool)