# deck_gen_data.py
from dataclasses import dataclass, asdict
import json
import os

@dataclass
class DeckGenData:
    input_folder: str = "assets/input"
    output_folder: str = "out/deck1"
    prefix_string: str = "poker_deck"
    design_params: dict = None

    def __post_init__(self):
        if self.design_params is None:
            self.design_params = {
                "Design": {
                    "Preview index": 42,
                    "Outer border": 10,
                    "Inner border": 400
                }
            }

    def get_save_file(self):
        return os.path.join(self.output_folder, f"{self.prefix_string}.json")

    def load(self):
        file_path = self.get_save_file()
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.__dict__.update(data)

    def save(self):
        file_path = self.get_save_file()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
