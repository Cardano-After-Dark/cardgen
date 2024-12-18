import requests
from PIL import Image
from io import BytesIO

class StabilityAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.host = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def generate_image(self, params):
        headers = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Convert all values to strings
        data = {k: str(v) for k, v in params.items()}

        # Send request as multipart/form-data
        response = requests.post(
            self.host,
            headers=headers,
            files={"none": ""},  # This forces the request to be multipart/form-data
            data=data
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        output_image = response.content
        finish_reason = response.headers.get("finish-reason")
        seed = response.headers.get("seed")

        if finish_reason == 'CONTENT_FILTERED':
            raise Warning("Generation failed NSFW classifier")

        return Image.open(BytesIO(output_image)), seed