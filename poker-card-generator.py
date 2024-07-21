from PIL import Image, ImageDraw, ImageFont
import os

class PokerCardGenerator:
    def __init__(self, front_bg, back_bg, font_path, font_size, symbol_images, face_images):
        self.front_bg = Image.open(front_bg)
        self.back_bg = Image.open(back_bg)
        self.font = ImageFont.truetype(font_path, font_size)
        self.symbols = {s: Image.open(img) for s, img in zip(['hearts', 'diamonds', 'spades', 'clubs'], symbol_images)}
        self.faces = {f: Image.open(img) for f, img in zip(['J', 'Q', 'K'], face_images)}

    def create_card(self, rank, suit):
        card = Image.new('RGB', (2496, 1872))
        front = self.front_bg.copy()
        draw = ImageDraw.Draw(front)

        # Add rank and suit
        symbol = self.symbols[suit]
        if rank in ['J', 'Q', 'K']:
            face = self.faces[rank]
            front.paste(face, (624 - face.width // 2, 936 - face.height // 2), face)
        else:
            draw.text((50, 50), rank, font=self.font, fill='black')
            draw.text((1198, 1822), rank, font=self.font, fill='black')
            front.paste(symbol, (624 - symbol.width // 2, 936 - symbol.height // 2), symbol)

        # Combine front and back
        card.paste(front, (0, 0))
        card.paste(self.back_bg, (1248, 0))

        return card

    def generate_deck(self, output_dir):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'spades', 'clubs']

        os.makedirs(output_dir, exist_ok=True)

        for suit in suits:
            for rank in ranks:
                card = self.create_card(rank, suit)
                card.save(f"{output_dir}/{rank}_of_{suit}.png")

if __name__ == "__main__":
    front_bg = "assets/gen/front_bg.png"
    back_bg = "assets/gen/back_bg.png"
    font_path = "assets/gen/Roboto-Bold.ttf"
    font_size = 100
    symbol_images = ["assets/gen/hearts.png", "assets/gen/diamonds.png", "assets/gen/spades.png", "assets/gen/clubs.png"]
    face_images = ["assets/gen/jack.png", "assets/gen/queen.png", "assets/gen/king.png"]

    generator = PokerCardGenerator(front_bg, back_bg, font_path, font_size, symbol_images, face_images)
    generator.generate_deck("output_cards")

    print("Deck generated successfully!")