import os
import glob
from dataclasses import dataclass, field
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont

@dataclass
class CardGeneratorInput:
    input_folder: str
    output_folder: str
    prefix_string: str
    n_card_gen: int
    back_image: Image.Image = None
    front_image: Image.Image = None
    suit_images: Dict[str, Image.Image] = field(default_factory=dict)
    font: ImageFont.FreeTypeFont = None

    def validate_input(self) -> bool:
        input_folder_full_path = os.path.abspath(self.input_folder)
        missing_files = []

        for file_pattern in CardGeneratorConstants.MANDATORY_FILES:
            if not glob.glob(os.path.join(self.input_folder, file_pattern)):
                missing_files.append(file_pattern)

        if missing_files:
            print(f"Missing input files: {', '.join(missing_files)} in folder {input_folder_full_path}")
            return False

        if not os.path.exists(self.output_folder):
            try:
                os.makedirs(self.output_folder)
            except OSError:
                print(f"Failed to create output folder: {self.output_folder}")
                return False

        if not 1 <= self.n_card_gen <= 52:
            print(f"Invalid number of cards to generate: {self.n_card_gen}. Must be between 1 and 52.")
            return False

        return True

    def initialize_assets(self):
        def load_last_image(pattern):
            images = sorted(glob.glob(os.path.join(self.input_folder, pattern)))
            return Image.open(images[-1])

        self.back_image = load_last_image("im-back*.png").resize(CardGeneratorConstants.HALF_CARD_SIZE)
        self.front_image = load_last_image("im-front*.png").resize(CardGeneratorConstants.HALF_CARD_SIZE)
        
        for suit in CardGeneratorConstants.SUITS:
            self.suit_images[suit] = load_last_image(f"suit-{suit}*.png").resize(CardGeneratorConstants.SUIT_SIZE)

        font_files = sorted(glob.glob(os.path.join(self.input_folder, "*.ttf")))
        print(f"Available fonts: {', '.join(os.path.basename(f) for f in font_files)}")
        self.font = ImageFont.truetype(font_files[-1], size=CardGeneratorConstants.FONT_SIZE)

class CardGeneratorConstants:
    MANDATORY_FILES = [
        "im-back*.png", "im-front*.png",
        "suit-heart*.png", "suit-diamond*.png", "suit-club*.png", "suit-spades*.png",
        "*.ttf"
    ]
    SUITS = ['heart', 'diamond', 'club', 'spades']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    CARD_SIZE = (2496, 1872)
    HALF_CARD_SIZE = (1248, 1872)
    SUIT_SIZE = (500, 500)
    FONT_SIZE = 100

class PokerCardGenerator:
    def __init__(self, input_data: CardGeneratorInput):
        self.input_data = input_data

    def generate_cards(self):
        card_count = 0

        for suit in CardGeneratorConstants.SUITS:
            for value in CardGeneratorConstants.VALUES:
                if card_count >= self.input_data.n_card_gen:
                    break

                canvas = Image.new('RGB', CardGeneratorConstants.CARD_SIZE)
                front = self.input_data.front_image.copy()
                draw = ImageDraw.Draw(front)

                color = 'red' if suit in ['heart', 'diamond'] else 'black'
                draw.text((50, 50), f"{value}\n{suit[0].upper()}", font=self.input_data.font, fill=color)
                draw.text((1198, 1822), f"{value}\n{suit[0].upper()}", font=self.input_data.font, fill=color, anchor="rs")

                suit_image = self.input_data.suit_images[suit]
                front.paste(suit_image, (374, 686), suit_image)

                canvas.paste(front, (0, 0))
                canvas.paste(self.input_data.back_image, (1248, 0))

                filename = f"{self.input_data.prefix_string}_{card_count+1:02d}_{suit}_{value}.png"
                canvas.save(os.path.join(self.input_data.output_folder, filename))
                print(f"Generated: {filename}")

                card_count += 1

            if card_count >= self.input_data.n_card_gen:
                break

        print(f"Generated {card_count} cards.")

# Example usage
input_data = CardGeneratorInput(
    input_folder="assets/input1",
    output_folder="out/deck1",
    prefix_string="poker_card",
    n_card_gen=15
)

if input_data.validate_input():
    input_data.initialize_assets()
    generator = PokerCardGenerator(input_data)
    generator.generate_cards()
else:
    print("Input validation failed. Please check your input and try again.")