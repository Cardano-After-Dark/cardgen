import tkinter as tk
from properties_io import PropertiesIO
from gen_io import GenIO
from img_gen_ui import ImgGenUI
from stability_ai_client import StabilityAIClient
from properties_io import PropertiesIO
from imgen_logger import logger as log
import os

class StabilityImGen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stability.ai Image Generator")

        props = PropertiesIO(os.path.expanduser("~/stability.ai.properties"))
        api_key = props.get_property('stability.ai.api.key')
        log.info(f"API key loaded: {len(api_key)} bytes")
        self.client = StabilityAIClient(api_key)

        self.gen_io = self.load_latest_gen_io()
        self.ui = ImgGenUI(self.root, self.gen_io, self.generate, self.save, self.load)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def load_latest_gen_io(self):
        try:
            log.info("Loading latest_genio file from .imgen")
            return GenIO.load(".imgen", "latest_genio")
        except FileNotFoundError:
            log.warning("No latest_genio file found, creating a new one")
            return GenIO()

    def generate(self, gen_io):
        log.info("Generating image with the following parameters: " + str(gen_io))
        params = {
            "prompt": gen_io.prompt,
            "negative_prompt": gen_io.negative_prompt,
            "aspect_ratio": gen_io.aspect_ratio,
            "seed": gen_io.seed,
            "output_format": gen_io.output_format
        }
        
        try:
            gen_io.gen_image, gen_io.seed = self.client.generate_image(params)
            log.info("Image generation successful")
            gen_io.gen_result = "Generation successful"
        except Exception as e:
            log.error(f"Error during image generation: {e}")
            gen_io.gen_result = str(e)

    def save(self, folder, prefix):
        log.info(f"Saving image to {folder}/{prefix}")
        os.makedirs(folder, exist_ok=True)
        self.gen_io.save(folder, prefix)

    def load(self, folder, prefix):
        log.info(f"Loading image from {folder}/{prefix}")
        return GenIO.load(folder, prefix)

    def on_closing(self):
        log.info("Closing >> Saving latest_genio file to .imgen")
        self.gen_io.save(".imgen", "latest_genio")
        self.root.destroy()

if __name__ == "__main__":
    StabilityImGen()