import os
import glob
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
from scipy import interpolate


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
    n_card_gen: int
    back_image: Image.Image = None
    front_image: Image.Image = None
    suit_images: Dict[str, Image.Image] = field(default_factory=dict)
    font: ImageFont.FreeTypeFont = None
    smoothness: float = CardGeneratorConstants.SMOOTHNESS
    curve_smoothness: int = 100  # Number of points for Bézier curve interpolation

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

        def extract_suit(image, suit):
            # Convert PIL Image to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find the largest contour (assuming it's the suit)
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Simplify the contour
            epsilon = 0.005 * cv2.arcLength(largest_contour, True)
            approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)
            
            # Convert to numpy array and reshape
            points = approx_contour.reshape(-1, 2)
            
            # Create a periodic spline
            tck, u = interpolate.splprep([points[:, 0], points[:, 1]], s=0, per=True)
            
            # Generate new points along the spline
            new_points = interpolate.splev(np.linspace(0, 1, self.curve_smoothness), tck)
            
            # Scale and translate the points
            x, y, w, h = cv2.boundingRect(approx_contour)
            scale = min(CardGeneratorConstants.SUIT_SIZE[0] / w, CardGeneratorConstants.SUIT_SIZE[1] / h)
            translate_x = (CardGeneratorConstants.SUIT_SIZE[0] - w * scale) / 2 - x * scale
            translate_y = (CardGeneratorConstants.SUIT_SIZE[1] - h * scale) / 2 - y * scale
            
            scaled_points = [(p[0] * scale + translate_x, p[1] * scale + translate_y) for p in zip(*new_points)]
            
            # Create a new image with transparent background
            new_img = Image.new('RGBA', CardGeneratorConstants.SUIT_SIZE, (0, 0, 0, 0))
            draw = ImageDraw.Draw(new_img)
            
            # Draw and fill the contour
            color = CardGeneratorConstants.RED_COLOR if suit in ['heart', 'diamond'] else CardGeneratorConstants.BLACK_COLOR
            draw.polygon(scaled_points, fill=color, outline=color)
            
            return new_img

        self.back_image = load_last_image("im-back*.png").resize(CardGeneratorConstants.HALF_CARD_SIZE)
        self.front_image = load_last_image("im-front*.png").resize(CardGeneratorConstants.HALF_CARD_SIZE)
        
        for suit in CardGeneratorConstants.SUITS:
            suit_image = load_last_image(f"suit-{suit}*.png")
            self.suit_images[suit] = extract_suit(suit_image, suit)

        font_files = sorted(glob.glob(os.path.join(self.input_folder, "*.ttf")))
        print(f"Available fonts: {', '.join(os.path.basename(f) for f in font_files)}")
        self.font = ImageFont.truetype(font_files[-1], size=CardGeneratorConstants.FONT_SIZE)




class PokerCardGenerator:
    def __init__(self, input_data: CardGeneratorInput):
        self.input_data = input_data

    def create_stacked_value_suit(self, value: str, suit: str, font: ImageFont.FreeTypeFont, color: str) -> Image.Image:
        # Create a new image with RGBA mode (for transparency)
        img_size = (font.size * 2, font.size * 3)  # Adjust size as needed
        img = Image.new('RGBA', img_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Draw the value
        value_bbox = draw.textbbox((0, 0), value, font=font)
        value_width = value_bbox[2] - value_bbox[0]
        value_height = value_bbox[3] - value_bbox[1]
        value_position = ((img_size[0] - value_width) // 2, 0)
        draw.text(value_position, value, font=font, fill=color)

        # Resize and draw the suit
        suit_image = self.input_data.suit_images[suit].copy()
        suit_image = suit_image.resize((value_width, value_width), Image.LANCZOS)
        suit_position = ((img_size[0] - value_width) // 2, value_height + font.size // 2)
        img.paste(suit_image, suit_position, suit_image)

        return img

    def generate_cards(self):
        card_count = 0

        suit_abbreviations = {'heart': 'H', 'diamond': 'D', 'club': 'C', 'spades': 'S'}

        for suit in CardGeneratorConstants.SUITS:
            for value in CardGeneratorConstants.VALUES:
                if card_count >= self.input_data.n_card_gen:
                    break

                canvas = Image.new('RGB', CardGeneratorConstants.CARD_SIZE)
                front = self.input_data.front_image.copy()
                
                color = CardGeneratorConstants.RED_COLOR if suit in ['heart', 'diamond'] else CardGeneratorConstants.BLACK_COLOR
                
                # Create stacked value-suit for top-left
                stacked_image_top = self.create_stacked_value_suit(value, suit, self.input_data.font, color)
                front.paste(stacked_image_top, (50, 50), stacked_image_top)
                
                # Create stacked value-suit for bottom-right (rotated 180 degrees)
                stacked_image_bottom = self.create_stacked_value_suit(value, suit, self.input_data.font, color)
                stacked_image_bottom = stacked_image_bottom.rotate(180)
                front.paste(stacked_image_bottom, (1198 - stacked_image_bottom.width, 1822 - stacked_image_bottom.height), stacked_image_bottom)

                # Add the large central suit image
                suit_image = self.input_data.suit_images[suit].copy()
                central_suit_size = (500, 500)  # Adjust this size as needed
                suit_image = suit_image.resize(central_suit_size, Image.LANCZOS)
                suit_position = ((CardGeneratorConstants.HALF_CARD_SIZE[0] - central_suit_size[0]) // 2,
                                 (CardGeneratorConstants.HALF_CARD_SIZE[1] - central_suit_size[1]) // 2)
                front.paste(suit_image, suit_position, suit_image)

                canvas.paste(front, (0, 0))
                canvas.paste(self.input_data.back_image, (1248, 0))

                # New naming convention
                suit_abbr = suit_abbreviations[suit]
                filename = f"{self.input_data.prefix_string}_{card_count+1:02d}_{value}_{suit_abbr}.png"
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
    n_card_gen=3
)

if input_data.validate_input():
    input_data.initialize_assets()
    generator = PokerCardGenerator(input_data)
    generator.generate_cards()
else:
    print("Input validation failed. Please check your input and try again.")