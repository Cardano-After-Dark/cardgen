import base64
from PIL import Image
from io import BytesIO

class AIImageGen:
    def __init__(self):
        self.parameters = {
            'prompt': '',
            'negative_prompt': '',
            'aspect_ratio': '2:3',
            'seed': 0,
            'output_format': 'png'
        }
        self.generated_image = None
        self.generation_result = ''

    def generate_image(self):
        # Placeholder for actual image generation
        # In a real implementation, this would call an AI model or API
        self.generated_image = Image.new('RGB', (300, 450), color='lightgray')
        self.generation_result = "Image generated successfully"
        return self.generated_image, self.generation_result

    def save_image(self, folder, prefix):
        if self.generated_image:
            filename = f"{folder}/{prefix}_{self.parameters['seed']}.{self.parameters['output_format']}"
            self.generated_image.save(filename)
            return filename
        return None

    def load_image(self, filename):
        self.generated_image = Image.open(filename)
        return self.generated_image

    def get_image_base64(self):
        if self.generated_image:
            buffered = BytesIO()
            self.generated_image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
        return None

    def set_parameters(self, **kwargs):
        self.parameters.update(kwargs)

    def get_parameters(self):
        return self.parameters
