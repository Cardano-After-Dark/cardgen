# deck_gen_controller.py
import os
import tkinter as tk
from tkinter import messagebox
from deck_gen_data import DeckGenData
from deck_gen_gui import DeckGenGui
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeckGenController:
    def __init__(self, root):
        self.model = DeckGenData()
        self.view = DeckGenGui(root, self.model)
        
        # Connect GUI actions to controller methods
        self.view.load_parameters = self.load
        self.view.save_parameters = self.save
        self.view.preview_deck = self.preview
        self.view.generate_deck = self.generate

    def log(self, message):
        logging.info(message)
        self.view.log(message)

    def load(self):
        path = self.model.get_save_file()
        if os.path.exists(path):
            self.model.load()
            self.view.update_from_model()
            self.log(f"[INFO] Loaded configuration from {path}")
        else:
            self.log(f"[WARN] No configuration file found at {path}")

    def save(self):
        path = self.model.get_save_file()
        if os.path.exists(path):
            if messagebox.askyesno("Overwrite", f"File {path} already exists. Overwrite?"):
                self.model.save()
                self.log(f"[INFO] Saved configuration to {path}")
            else:
                self.log("[INFO] Save operation cancelled")
        else:
            self.model.save()
            self.log(f"[INFO] Saved configuration to {path}")

    def preview(self):
        preview_window = tk.Toplevel(self.view.master)
        preview_window.title("Preview")
        tk.Label(preview_window, text="Image preview placeholder").pack()
        self.log("[INFO] Preview generated")

    def generate(self):
        self.log(f"[INFO] Generated deck {self.model.prefix_string} into {self.model.output_folder}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGenController(root)
    root.mainloop()