import json
from typing import Any, Type
import openai
import requests
import os


class GenerateAndDownloadImageSchema(BaseModel):
    """
    Schema defining the arguments for generating and downloading an image.
    """
    prompt: str = Field(..., description="Text prompt describing the image you want DALL·E to create.")
    file_name: str = Field(..., description="Local file name (or path) where the generated image is saved.")
    size: str = Field("...", description="Resolution of the generated image, e.g. '1024x1024'.")
    response_format: str = Field("url", description="Either 'url' or 'b64_json'. 'url' is default.")
    # If you want to specify a particular model (e.g., 'dall-e-3'), add:
    # model: str = Field("image-alpha-001", description="The DALL·E model name if needed.")

class GenerateAndDownloadImageTool(BaseTool):
    """
    A single tool that generates an image using OpenAI's DALL·E API and downloads it locally.
    """
    name: str = "generate_and_download_image"
    id: str = "generate_and_download_image"
    description: str = (
        "Generate an image from a prompt via DALL·E, then download the resulting image to file."
    )
    args_schema: Type[BaseModel] = GenerateAndDownloadImageSchema

    def _run(self, **kwargs) -> Any:
        prompt = kwargs["prompt"]
        file_name = kwargs["file_name"]
        n = 1
        size = kwargs.get("size", "1024x1024")
        response_format = kwargs.get("response_format", "url")
        # model = kwargs.get("model", "image-alpha-001") # If you want a specific model param

        # Make sure your OPENAI_API_KEY is set
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            return "OPENAI_API_KEY is not set in the environment."

        try:
            # Configure OpenAI
            openai.api_key = openai_api_key
            client = openai.OpenAI(api_key=openai_api_key)

            response = client.images.generate(
                prompt=prompt,
                n=n,
                size=size,
                response_format=response_format,
                model="dall-e-3", 
            )

            # We'll just take the first generated image
            # If response_format="url", we get a URL for the image.
            # If "b64_json", we get a base64-encoded string.
            response_dict = response.model_dump(mode="python")
            if not response_dict or "data" not in response_dict or len(response_dict["data"]) == 0:
                return "No image data returned from DALL·E."
            image_url = response_dict["data"][0]["url"]

            # Depending on the response format, extract the image data
            if response_format == "url":
                image_url = response_dict["data"][0]["url"]
                # Download the image from the URL
                r = requests.get(image_url)
                r.raise_for_status()  # Raise an error if the HTTP request failed
                with open(file_name, "wb") as f:
                    f.write(r.content)
                return json.dumps({
                    "message": f"Image generated and saved as {file_name}",
                    "url": image_url
                }, indent=2)
            else:
                # If response_format is "b64_json", decode the base64 data and write it to file
                b64_data = response_dict["data"][0]["b64_json"]
                image_bytes = b64_data.encode("utf-8")  # Convert string to bytes
                import base64
                decoded = base64.decodebytes(image_bytes)
                with open(file_name, "wb") as f:
                    f.write(decoded)
                return json.dumps({
                    "message": f"Image generated (base64) and saved as {file_name}"
                }, indent=2)

        except Exception as e:
            return f"Image generation or download failed: {e}"

    async def _arun(self, **kwargs) -> Any:
        return self._run(**kwargs)
