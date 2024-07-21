# imgen/gen_io.py
import os
import json
from dataclasses import dataclass, asdict, field
from typing import Optional
# from imgen_logger import logger as log
from PIL import Image

@dataclass
class GenIO:
    prompt: str = ""
    negative_prompt: str = ""
    aspect_ratio: str = "2:3"
    seed: int = 0
    output_format: str = "png"
    gen_result: str = ""
    gen_image: Optional[Image.Image] = None

    def save(self, path: str, prefix: str):
        params = asdict(self)
        del params['gen_image']  # Remove gen_image from params as it's not JSON serializable

        # log.info(f"Saving params to {path}/{prefix}_params.json")
        with open(f"{path}/{prefix}_params.json", 'w') as f:
            json.dump(params, f)

        if self.gen_image:
            # log.info(f"Saving image to {path}/{prefix}_img.{self.output_format}")
            self.gen_image.save(f"{path}/{prefix}_img.{self.output_format}")
        # log.info("Save complete")

    @classmethod
    def load(cls, path: str, prefix: str):
        # log.info(f"Loading params from {path}/{prefix}_params.json")
        with open(f"{path}/{prefix}_params.json", 'r') as f:
            params = json.load(f)

        gen_image = None
        image_path = f"{path}/{prefix}_img.{params['output_format']}"
        if os.path.exists(image_path):
            # log.info(f"Loading image from {image_path}")
            gen_image = Image.open(image_path)
        
        # log.info("Load complete")

        return cls(**params, gen_image=gen_image)