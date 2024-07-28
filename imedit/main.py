# main.py
import tkinter as tk
from deck_gen_controller import DeckGenController

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGenController(root)
    root.mainloop()