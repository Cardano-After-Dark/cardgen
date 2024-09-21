# deck_gen_gui.py
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import json  # Add this import
from deck_gen_data import DeckGenData

class DeckGenGui:
    def __init__(self, master, model: DeckGenData):
        self.master = master
        self.model = model
        master.title("Deck Generator")
        master.geometry("400x600")

        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.create_generation_section()
        self.create_design_section()
        self.create_actions_section()
        self.create_log_section()

        # self.create_widgets()
        self.update_from_model()

    def create_generation_section(self):
        generation_frame = ttk.LabelFrame(self.main_frame, text="Generation", padding="10")
        generation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.main_frame.columnconfigure(0, weight=1)

        # Input folder
        ttk.Label(generation_frame, text="Input folder:").grid(row=0, column=0, sticky=tk.W)
        self.input_entry = ttk.Entry(generation_frame)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(generation_frame, text="select", command=self.select_input_folder).grid(row=0, column=2, padx=(5, 0))

        # Output folder
        ttk.Label(generation_frame, text="Output folder:").grid(row=1, column=0, sticky=tk.W)
        self.output_entry = ttk.Entry(generation_frame)
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Button(generation_frame, text="select", command=self.select_output_folder).grid(row=1, column=2, padx=(5, 0))

        # Prefix string
        ttk.Label(generation_frame, text="Prefix string:").grid(row=2, column=0, sticky=tk.W)
        self.prefix_entry = ttk.Entry(generation_frame)
        self.prefix_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

        generation_frame.columnconfigure(1, weight=1)

    def create_design_section(self):
        design_frame = ttk.LabelFrame(self.main_frame, text="Design", padding="10")
        design_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.main_frame.rowconfigure(1, weight=1)

        self.design_text = scrolledtext.ScrolledText(design_frame, wrap=tk.WORD, height=10)
        self.design_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        design_frame.columnconfigure(0, weight=1)
        design_frame.rowconfigure(0, weight=1)

    def create_actions_section(self):
        actions_frame = ttk.LabelFrame(self.main_frame, text="Actions", padding="10")
        actions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(actions_frame, text="Parameters").grid(row=0, column=0, sticky=tk.W)
        self.load_button = ttk.Button(actions_frame, text="load")
        self.load_button.grid(row=0, column=1, padx=(5, 0))
        self.save_button = ttk.Button(actions_frame, text="save")
        self.save_button.grid(row=0, column=2, padx=(5, 0))

        ttk.Label(actions_frame, text="Deck").grid(row=1, column=0, sticky=tk.W)
        self.preview_button = ttk.Button(actions_frame, text="preview")
        self.preview_button.grid(row=1, column=1, padx=(5, 0))
        self.generate_button = ttk.Button(actions_frame, text="generate")
        self.generate_button.grid(row=1, column=2, padx=(5, 0))

    def create_log_section(self):
        log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.rowconfigure(3, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def update_from_model(self):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.model.input_folder)
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.model.output_folder)
        self.prefix_entry.delete(0, tk.END)
        self.prefix_entry.insert(0, self.model.prefix_string)
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
    def set_load_callback(self, callback):
        self.load_button.config(command=callback)

    def set_save_callback(self, callback):
        self.save_button.config(command=callback)

    def set_preview_callback(self, callback):
        self.preview_button.config(command=callback)

    def set_generate_callback(self, callback):
        self.generate_button.config(command=callback)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
