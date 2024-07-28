# deck_gen_gui.py
import tkinter as tk
from tkinter import filedialog, scrolledtext
import json  # Add this import
from deck_gen_data import DeckGenData

class DeckGenGui:
    def __init__(self, master, model: DeckGenData):
        self.master = master
        self.model = model
        master.title("Deck Generator")

        self.create_widgets()
        self.update_from_model()

    def create_widgets(self):
        # Generation section
        tk.Label(self.master, text="Generation").grid(row=0, column=0, sticky="w")

        tk.Label(self.master, text="Input folder:").grid(row=1, column=0, sticky="w")
        self.input_folder = tk.Entry(self.master)
        self.input_folder.grid(row=1, column=1)
        tk.Button(self.master, text="select", command=self.select_input_folder).grid(row=1, column=2)

        tk.Label(self.master, text="Output folder:").grid(row=2, column=0, sticky="w")
        self.output_folder = tk.Entry(self.master)
        self.output_folder.grid(row=2, column=1)
        tk.Button(self.master, text="select", command=self.select_output_folder).grid(row=2, column=2)

        tk.Label(self.master, text="Prefix string:").grid(row=3, column=0, sticky="w")
        self.prefix_string = tk.Entry(self.master)
        self.prefix_string.grid(row=3, column=1)

        # Design section
        tk.Label(self.master, text="Design").grid(row=4, column=0, sticky="w")
        self.design_text = scrolledtext.ScrolledText(self.master, height=10)
        self.design_text.grid(row=5, column=0, columnspan=3)

        # Actions section
        tk.Label(self.master, text="Actions").grid(row=6, column=0, sticky="w")

        tk.Label(self.master, text="Parameters").grid(row=7, column=0, sticky="w")
        tk.Button(self.master, text="load", command=self.load).grid(row=7, column=1)
        tk.Button(self.master, text="save", command=self.save).grid(row=7, column=2)

        tk.Label(self.master, text="Deck").grid(row=8, column=0, sticky="w")
        tk.Button(self.master, text="preview", command=self.preview).grid(row=8, column=1)
        tk.Button(self.master, text="generate", command=self.generate).grid(row=8, column=2)

        # Log section
        tk.Label(self.master, text="Log").grid(row=9, column=0, sticky="w")
        self.log_text = scrolledtext.ScrolledText(self.master, height=5)
        self.log_text.grid(row=10, column=0, columnspan=3)

    def update_from_model(self):
        self.input_folder.delete(0, tk.END)
        self.input_folder.insert(0, self.model.input_folder)

        self.output_folder.delete(0, tk.END)
        self.output_folder.insert(0, self.model.output_folder)

        self.prefix_string.delete(0, tk.END)
        self.prefix_string.insert(0, self.model.prefix_string)

        self.design_text.delete('1.0', tk.END)
        self.design_text.insert(tk.END, json.dumps(self.model.design_params, indent=2))

    def select_input_folder(self):
        folder = filedialog.askdirectory(initialdir=self.model.input_folder)
        if folder:
            self.model.input_folder = folder
            self.update_from_model()

    def select_output_folder(self):
        folder = filedialog.askdirectory(initialdir=self.model.output_folder)
        if folder:
            self.model.output_folder = folder
            self.update_from_model()

    # Placeholder methods to be connected to the controller
    def load(self):
        pass

    def save(self):
        pass

    def preview(self):
        pass

    def generate(self):
        pass

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
