import json
from PIL import Image

class GenIO:
    def __init__(self, prompt="", negative_prompt="", aspect_ratio="2:3", seed=0, output_format="png", gen_result=""):
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.aspect_ratio = aspect_ratio
        self.seed = seed
        self.output_format = output_format
        self.gen_result = gen_result
        self.gen_image = None

    def save(self, folder, prefix):
        params = {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "aspect_ratio": self.aspect_ratio,
            "seed": self.seed,
            "output_format": self.output_format,
            "gen_result": self.gen_result
        }
        
        with open(f"{folder}/{prefix}_params.json", "w") as f:
            json.dump(params, f)
        
        if self.gen_image:
            self.gen_image.save(f"{folder}/{prefix}_img.{self.output_format}")

    @classmethod
    def load(cls, folder, prefix):
        with open(f"{folder}/{prefix}_params.json", "r") as f:
            params = json.load(f)
        
        gen_io = cls(**params)
        
        try:
            gen_io.gen_image = Image.open(f"{folder}/{prefix}_img.{params['output_format']}")
        except FileNotFoundError:
            pass
        
        return gen_io