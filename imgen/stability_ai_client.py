# imgen/stability_ai_client.py

import requests
import json
import time
from PIL import Image
from io import BytesIO

class StabilityAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        # self.host = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def send_generation_request(self, host, params):
        headers = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self.api_key}"
        }

        print(f"Sending request to {host} with params: {params}")
        response = requests.post(host, headers=headers, data=params)

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        return response

    def process_response(self, response):
        output_image = Image.open(BytesIO(response.content))
        finish_reason = response.headers.get("finish-reason")
        seed = response.headers.get("seed")

        if finish_reason == 'CONTENT_FILTERED':
            raise Warning("Generation failed NSFW classifier")

        return output_image, seed
