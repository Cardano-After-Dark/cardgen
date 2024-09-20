import os
import glob
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import json
from PIL import Image, ImageOps, ImageDraw, ImageFont
import numpy as np
import cv2
from scipy import interpolate
import yaml
import traceback

DEFAULT_CONFIG = """
input_folder: "assets/input1"
output_folder: "out/deck1"
prefix_string: "poker_card"
app_params:
  Design:
    Preview index: 42
    card value margin: 10
    card value padding: 10
    main suit scale: 1
    main face scale: 1
"""

class CardConstants:
    MANDATORY_FILES = [
        "im-back*.png", "im-front*.png",
        "suit-heart*.png", "suit-diamond*.png", "suit-club*.png", "suit-spades*.png",
        "*.ttf"
    ]
    SUITS = ['heart', 'diamond', 'club', 'spades']
    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    CARD_SIZE = (2496, 1872)
    HALF_CARD_SIZE = (1248, 1872)
    SUIT_SIZE = (700, 700)
    FONT_SIZE = 200
    RED_COLOR = (255, 0, 255)  # RGB for red
    BLACK_COLOR = (60, 60, 60)  # RGB for black
    SMOOTHNESS = 0.0001  # Suit contour smoothness (0.01 to 0.05 is a good range)

@dataclass
class CardGeneratorInput:
    input_folder: str
    output_folder: str
    prefix_string: str
    n_card_gen: int = 52
    back_image: Image.Image = None
    front_image: Image.Image = None
    suit_images: Dict[str, Image.Image] = field(default_factory=dict)
    font: ImageFont.FreeTypeFont = None
    smoothness: float = CardConstants.SMOOTHNESS
    curve_smoothness: int = 100  # Number of points for Bézier curve interpolation

    def validate_input(self) -> bool:
        input_folder_full_path = os.path.abspath(self.input_folder)
        missing_files = []

        for file_pattern in CardConstants.MANDATORY_FILES:
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

    def initialize_assets(self, parameters):
        def load_last_image(pattern):
            images = sorted(glob.glob(os.path.join(self.input_folder, pattern)))
            return Image.open(images[-1])

        def extract_suit(image, suit, parameters):
            """Transform a transparent PNG suit image"""
            scale = parameters["app_params"]["Design"].get("main suit scale", 1)
            recolor = parameters["app_params"]["Design"].get("recolor main suit", True)

            print(f"extract_suit: {suit}, scale={scale}, recolor={recolor}")

            original_size = image.size

            if recolor:
                color = CardConstants.RED_COLOR if suit in ['heart', 'diamond'] else CardConstants.BLACK_COLOR
                # Convert color tuple to RGB
                rgb_color = tuple(color[:3])  # Take only the RGB values, ignore alpha if present
                # Create a grayscale version of the image
                gray_image = ImageOps.grayscale(image)
                # Colorize the grayscale image
                colored_image = ImageOps.colorize(gray_image, (0, 0, 0), rgb_color)
                # Preserve the alpha channel from the original image
                colored_image.putalpha(image.getchannel('A'))
                image = colored_image

            # Scale the image
            if scale != 1:
                new_size = tuple(int(dim * scale) for dim in original_size)
                image = image.resize(new_size, Image.LANCZOS)

            print(f"Original size: {original_size}, New size: {image.size}")

            return image

        self.back_image = load_last_image("im-back*.png").resize(CardConstants.HALF_CARD_SIZE)
        self.front_image = load_last_image("im-front*.png").resize(CardConstants.HALF_CARD_SIZE)
        
        for suit in CardConstants.SUITS:
            suit_image = load_last_image(f"suit-{suit}*.png")
            self.suit_images[suit] = extract_suit(suit_image, suit, parameters)

        font_files = sorted(glob.glob(os.path.join(self.input_folder, "*.ttf")))
        print(f"Available fonts: {', '.join(os.path.basename(f) for f in font_files)}")
        self.font = ImageFont.truetype(font_files[-1], size=CardConstants.FONT_SIZE)

class DeckGen:
    """Initialize class with given parameters or default values."""
    def __init__(self, parameters=None):
        self.parameters = parameters or yaml.safe_load(DEFAULT_CONFIG)
        self.input_data = None
        self.generator = None

    def loadParams(self, parameters):
        self.parameters = parameters
        self.input_data = CardGeneratorInput(
            input_folder=self.parameters["input_folder"],
            output_folder=self.parameters["output_folder"],
            prefix_string=self.parameters["prefix_string"],
            n_card_gen=52  # Default to generating full deck
        )
        if self.input_data.validate_input():
            self.input_data.initialize_assets(self.parameters)
            self.generator = PokerCardGenerator(self.input_data)
        else:
            raise ValueError("Input validation failed. Please check your parameters and try again.")

    def generate_deck(self, stop_callback=None):
        if not self.generator:
            raise ValueError("Parameters not loaded. Call loadParams() first.")
        self.generator.generate_cards(stop_callback)

    def preview_card(self, card_number=None):
        if not self.generator:
            raise ValueError("Parameters not loaded. Call loadParams() first.")
            
        preview_index = card_number if card_number is not None else self.parameters["app_params"]["Design"].get("Preview index", 0)
        preview_image = self.generator.generate_card_image(preview_index, return_image=True)
        if not isinstance(preview_image, Image.Image):
            raise ValueError("Failed to generate preview image")
        return preview_image

class PokerCardGenerator:
    def __init__(self, input_data: CardGeneratorInput):
        self.input_data = input_data

    def create_stacked_value_suit(self, value: str, suit: str, color: str) -> Image.Image:
        # Create a new image with RGBA mode (for transparency)
        img_size = (self.input_data.font.size * 2, self.input_data.font.size * 3)  # Adjust size as needed
        img = Image.new('RGBA', img_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Draw the value
        value_bbox = draw.textbbox((0, 0), value, font=self.input_data.font)
        value_width = value_bbox[2] - value_bbox[0]
        value_height = value_bbox[3] - value_bbox[1]
        value_position = ((img_size[0] - value_width) // 2, 0)
        draw.text(value_position, value, font=self.input_data.font, fill=color)

        # Resize and draw the suit
        suit_image = self.input_data.suit_images[suit].copy()
        suit_image = suit_image.resize((value_width, value_width), Image.LANCZOS)
        suit_position = ((img_size[0] - value_width) // 2, value_height + self.input_data.font.size // 2)
        img.paste(suit_image, suit_position, suit_image)

        return img

    def generate_cards(self, stop_callback=None):
        card_count = 0
        suit_abbreviations = {'heart': 'H', 'diamond': 'D', 'club': 'C', 'spades': 'S'}

        for suit in CardConstants.SUITS:
            for value in CardConstants.VALUES:
                if card_count >= self.input_data.n_card_gen:
                    break

                if stop_callback and stop_callback():
                    print("Card generation stopped by user")
                    return

                self.generate_card_image(card_count, suit_abbreviations, suit, value)
                card_count += 1

            if card_count >= self.input_data.n_card_gen:
                break

        print(f"Generated {card_count} cards.")

    def generate_card_image(self, card_count, suit_abbreviations=None, suit=None, value=None, return_image=False):

        if suit_abbreviations is None:
            suit_abbreviations = {'heart': 'H', 'diamond': 'D', 'club': 'C', 'spades': 'S'}
        
        if suit is None or value is None:
            suit_index = card_count // 13
            value_index = card_count % 13
            suit = CardConstants.SUITS[suit_index]
            value = CardConstants.VALUES[value_index]

        canvas = Image.new('RGB', CardConstants.CARD_SIZE)
        front = self.input_data.front_image.copy()
                
        color = CardConstants.RED_COLOR if suit in ['heart', 'diamond'] else CardConstants.BLACK_COLOR
                
        # Create stacked value-suit for top-left
        stacked_image_top = self.create_stacked_value_suit(value, suit, color)
        front.paste(stacked_image_top, (50, 50), stacked_image_top)
                
        # Create stacked value-suit for bottom-right (rotated 180 degrees)
        stacked_image_bottom = self.create_stacked_value_suit(value, suit, color)
        stacked_image_bottom = stacked_image_bottom.rotate(180)
        front.paste(stacked_image_bottom, (1198 - stacked_image_bottom.width, 1822 - stacked_image_bottom.height), stacked_image_bottom)

        # Add the large central suit image
        suit_image = self.input_data.suit_images[suit].copy()
        central_suit_size = suit_image.size # get the image size
        suit_position = ((CardConstants.HALF_CARD_SIZE[0] - central_suit_size[0]) // 2,
                                (CardConstants.HALF_CARD_SIZE[1] - central_suit_size[1]) // 2)
        front.paste(suit_image, suit_position, suit_image)

        canvas.paste(front, (0, 0))
        canvas.paste(self.input_data.back_image, (1248, 0))

        if return_image:
            return canvas.copy()

        # New naming convention
        suit_abbr = suit_abbreviations[suit]
        filename = f"{self.input_data.prefix_string}_{card_count+1:02d}_{value}_{suit_abbr}.png"
        canvas.save(os.path.join(self.input_data.output_folder, filename))
        print(f"Generated: {filename}")

# used to get the image module
def get_image_module():
    return Image

if __name__ == "__main__":
    # Example usage as a command-line application
    deckgen = DeckGen()
    deckgen.loadParams(deckgen.parameters)  # Load default parameters
    deckgen.generate_deck()

    # Example of previewing a card
    preview_card = deckgen.preview_card()
    preview_card.show()  # This will display the preview card