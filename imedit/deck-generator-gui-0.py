import tkinter as tk
import ttkbootstrap as ttk
from tkinter import scrolledtext, filedialog, messagebox
from ttkbootstrap.tooltip import ToolTip
from dataclasses import dataclass, asdict, field
import json
from typing import Dict, Any
import os

@dataclass
class DeckGeneratorApp:
    input_folder: str = "assets/input1"
    output_folder: str = "out/deck1"
    prefix_string: str = "poker_card"
    design_params: Dict[str, Any] = field(default_factory=lambda: {
        "Design": {
            "Preview index": 42,
            "Outer border": 10,
            "Inner border": 400
        }
    })

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class DeckGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.app = DeckGeneratorApp()

        # Determine the system theme
        system_theme = "darkly" # or "cosmo"
        self.style = ttk.Style(theme=system_theme)

        master.title("Deck Generator")
        master.geometry("400x600")

        self.style.configure('TButton', width=7, padding=(5, 5))
        self.style.configure('Spaced.TFrame', padding=(0, 5))
        self.style.configure('Section.TLabelframe', padding=10)

        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.create_generation_section()
        self.create_design_section()
        self.create_actions_section()
        self.create_log_section()

        # Initialize GUI with default values
        self.update_gui_from_app()

    def create_generation_section(self):
        generation_frame = ttk.LabelFrame(self.main_frame, text="Generation", style='Section.TLabelframe')
        generation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.main_frame.columnconfigure(0, weight=1)

        # Input folder
        ttk.Label(generation_frame, text="Input folder:").grid(row=0, column=0, sticky=tk.W)
        self.input_entry = ttk.Entry(generation_frame)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        input_button = ttk.Button(generation_frame, text="select", command=self.select_input_folder)
        input_button.grid(row=0, column=2, padx=(5, 0))
        ToolTip(input_button, text="Select the input folder containing card assets")

        # Output folder
        ttk.Label(generation_frame, text="Output folder:").grid(row=1, column=0, sticky=tk.W)
        self.output_entry = ttk.Entry(generation_frame)
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        output_button = ttk.Button(generation_frame, text="select", command=self.select_output_folder)
        output_button.grid(row=1, column=2, padx=(5, 0))
        ToolTip(output_button, text="Select the output folder for generated cards")

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
        load_button = ttk.Button(actions_frame, text="load", command=self.load_parameters)
        load_button.grid(row=0, column=1, padx=(5, 0))
        ToolTip(load_button, text="Load parameters from a JSON file")

        save_button = ttk.Button(actions_frame, text="save", command=self.save_parameters)
        save_button.grid(row=0, column=2, padx=(5, 0))
        ToolTip(save_button, text="Save current parameters to a JSON file")

        ttk.Label(actions_frame, text="Deck").grid(row=1, column=0, sticky=tk.W)
        preview_button = ttk.Button(actions_frame, text="preview", command=self.preview_deck)
        preview_button.grid(row=1, column=1, padx=(5, 0))
        ToolTip(preview_button, text="Preview the deck with current settings")

        generate_button = ttk.Button(actions_frame, text="generate", command=self.generate_deck)
        generate_button.grid(row=1, column=2, padx=(5, 0))
        ToolTip(generate_button, text="Generate the deck with current settings")

    def create_log_section(self):
        log_frame = ttk.LabelFrame(self.main_frame, text="Log", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.rowconfigure(3, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)
            self.app.input_folder = folder

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            self.app.output_folder = folder

    def load_parameters(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.app = DeckGeneratorApp.from_dict(data)
                self.update_gui_from_app()
                self.log("Parameters loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load parameters: {str(e)}")

    def save_parameters(self):
        self.update_app_from_gui()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.app.to_dict(), f, indent=2)
                self.log("Parameters saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save parameters: {str(e)}")

    def preview_deck(self):
        self.update_app_from_gui()
        preview_window = tk.Toplevel(self.master)
        preview_window.title("Deck Preview")
        preview_label = ttk.Label(preview_window, text="Generic Image Placeholder")
        preview_label.pack(padx=20, pady=20)
        self.log(f"[INFO] deck preview {self.app.prefix_string}")

    def generate_deck(self):
        self.update_app_from_gui()
        self.log(f"[INFO] deck generated {self.app.prefix_string} into {self.app.output_folder}")

    def update_gui_from_app(self):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.app.input_folder)
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.app.output_folder)
        self.prefix_entry.delete(0, tk.END)
        self.prefix_entry.insert(0, self.app.prefix_string)
        self.design_text.delete('1.0', tk.END)
        self.design_text.insert(tk.END, json.dumps(self.app.design_params, indent=2))

    def update_app_from_gui(self):
        self.app.input_folder = self.input_entry.get()
        self.app.output_folder = self.output_entry.get()
        self.app.prefix_string = self.prefix_entry.get()
        try:
            self.app.design_params = json.loads(self.design_text.get('1.0', tk.END))
        except json.JSONDecodeError:
            self.app.design_params = None

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGeneratorGUI(root)
    root.mainloop()
