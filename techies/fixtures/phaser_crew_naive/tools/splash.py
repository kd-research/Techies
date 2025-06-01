from techies.predefined_tools.base_tool import BaseTool, BaseModel, Type, Field
import os
import base64
from openai import OpenAI

class SplashToolSchema(BaseModel):
    splash_description: str = Field(
        type=str,
        description="Description of the splash screen image to generate."
    )

class SplashTool(BaseTool):
    name: str = "Splash screen generator"
    id: str = "splash_gen"
    description: str = "Create splash screen images for a game app."
    args_schema: Type[BaseModel] = SplashToolSchema
    base_dir: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _run(self, splash_description: str) -> str:
        client: OpenAI = OpenAI()

        # make external directory if not exists
        os.makedirs(os.path.join(self.base_dir, "external"), exist_ok=True)
        splash_path = os.path.join(self.base_dir, "external", "splash.png")

        # Generate splash screen image
        splash_img = client.images.generate(
            model="dall-e-3",
            prompt="Create a game app splash screen image for the description:\n"+splash_description,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        image_bytes = base64.b64decode(splash_img.data[0].b64_json)
        with open(splash_path, "wb") as f:
            f.write(image_bytes)
        return f"Splash screen image generated successfully."
    
register_tool(SplashTool)