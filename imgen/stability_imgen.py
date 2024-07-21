from properties_io import PropertiesIO
from gen_io import GenIO
from img_gen_ui import ImgGenUI
from stability_ai_client import StabilityAIClient
import os

class StabilityImGen:
    def __init__(self):
        props = PropertiesIO('cardgen.properties')
        api_key = props.get_property('stability.ai.api.key')
        self.client = StabilityAIClient(api_key)
        
        self.gen_io = self.load_or_create_genio()
        self.ui = ImgGenUI(self.gen_io, self.client)

    def load_or_create_genio(self):
        genio = GenIO.load(".imgen", "latest_genio")
        if genio is None:
            genio = GenIO()
        return genio

    def run(self):
        self.ui.run()
        self.save_current_genio()

    def save_current_genio(self):
        os.makedirs(".imgen", exist_ok=True)
        self.gen_io.save(".imgen", "latest_genio")

if __name__ == "__main__":
    app = StabilityImGen()
    app.run()
