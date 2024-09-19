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
    app_params: Dict[str, Any] = None

    def __post_init__(self):
        if self.app_params is None:
            self.app_params = {
                "Design": {
                    "Preview index": 42,
                    "Outer border": 10,
                    "Inner border": 400
                }
            }

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def get_save_file(self):
        return os.path.join(self.output_folder, f"{self.prefix_string}.json")        

class DeckGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.app = DeckGeneratorApp()
        self.preview_window = None # store preview window reference

        self.style = ttk.Style(theme="cosmo")  # "darkly" or "cosmo"
        master.title("Deck Generator")
        master.geometry("400x600")
        master.minsize(400, 600)  # Set minimum size

        self.style.configure('TButton', width=10)
        self.style.configure('TEntry', padding=5)
        self.style.configure('TLabel', padding=5)

        self.main_frame = ttk.Frame(master, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.create_sections()

        # Initialize GUI with default values
        self.update_gui_from_app()
    
    def create_sections(self):
        sections = [
            ("Generation", self.create_generation_section),
            ("Params", self.create_params_section),
            ("Actions", self.create_actions_section),
            ("Log", self.create_log_section)
        ]
        for i, (title, create_func) in enumerate(sections):
            frame = ttk.LabelFrame(self.main_frame, text=title, padding=10)
            frame.grid(row=i, column=0, sticky="nsew", pady=(0, 10))
            create_func(frame)
            self.main_frame.grid_rowconfigure(i, weight=1 if title in ["Design", "Log"] else 0)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_generation_section(self, parent):
        fields = [
            ("Input folder:", self.select_input_folder, "Select the input folder containing card assets"),
            ("Output folder:", self.select_output_folder, "Select the output folder for generated cards"),
            ("Prefix string:", None, None)
        ]
        for i, (label_text, command, tooltip) in enumerate(fields):
            ttk.Label(parent, text=label_text).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(parent)
            entry.grid(row=i, column=1, sticky="ew", padx=(5, 5), pady=2)
            setattr(self, f"{label_text.lower().replace(' ', '_').replace(':', '')}_entry", entry)
            if command:
                button = ttk.Button(parent, text="select", command=command)
                button.grid(row=i, column=2, padx=(5, 0), sticky="w") # sticky="w" aligns the button to the left
                if tooltip:
                    ToolTip(button, text=tooltip)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=0)  # Prevent button column from expanding

    def create_params_section(self, parent):
        self.params_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=10)
        self.params_text.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def create_actions_section(self, parent):
        actions = [
            ("Parameters", [("load", self.load_parameters), ("save", self.save_parameters)]),
            ("Deck", [("preview", self.preview_deck), ("generate", self.generate_deck)])
        ]
        for i, (label, buttons) in enumerate(actions):
            ttk.Label(parent, text=label).grid(row=i, column=0, sticky="w")
            for j, (text, command) in enumerate(buttons):
                button = ttk.Button(parent, text=text, command=command)
                button.grid(row=i, column=j+1, padx=(5, 0), sticky="w", pady=2) # align to left and add padding
                ToolTip(button, text=f"{text.capitalize()} {label.lower()}")
        parent.grid_columnconfigure(0, weight=0)  # Prevent label column from expanding
        parent.grid_columnconfigure(1, weight=0)  # Prevent first button column from expanding
        parent.grid_columnconfigure(2, weight=0)  # Prevent second button column from expanding
        parent.grid_columnconfigure(3, weight=1)  # Add an empty column to push buttons to the left

    def create_log_section(self, parent):
        self.log_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=10)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def select_input_folder(self):
        self.select_folder('input_folder_entry')

    def select_output_folder(self):
        self.select_folder('output_folder_entry')

    def select_folder(self, entry_name):
        folder = filedialog.askdirectory()
        if folder:
            getattr(self, entry_name).delete(0, tk.END)
            getattr(self, entry_name).insert(0, folder)
            setattr(self.app, entry_name.replace('_entry', ''), folder)


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

        # Close the existing preview window if it's open
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()

        self.preview_window = tk.Toplevel(self.master)
        self.preview_window.title("Deck Preview")
        self.preview_window.geometry("300x300") # default size
        self.preview_window.minsize(300, 300)  # Set minimum size

        # Position the preview window next to the main window
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        self.preview_window.geometry(f"+{main_x + main_width + 10}+{main_y}")

        preview_label = ttk.Label(self.preview_window, text="Generic Image Placeholder")
        preview_label.pack(padx=20, pady=20)
        self.log(f"[INFO] deck preview {self.app.prefix_string}")

    def generate_deck(self):
        self.update_app_from_gui()
        self.log(f"[INFO] deck generated {self.app.prefix_string} into {self.app.output_folder}")

    def update_gui_from_app(self):
        for attr in ['input_folder', 'output_folder', 'prefix_string']:
            getattr(self, f"{attr}_entry").delete(0, tk.END)
            getattr(self, f"{attr}_entry").insert(0, getattr(self.app, attr))
        self.params_text.delete('1.0', tk.END)
        self.params_text.insert(tk.END, json.dumps(self.app.app_params, indent=2))

    def update_app_from_gui(self):
        for attr in ['input_folder', 'output_folder', 'prefix_string']:
            setattr(self.app, attr, getattr(self, f"{attr}_entry").get())
        try:
            self.app.app_params = json.loads(self.params_text.get('1.0', tk.END))
        except json.JSONDecodeError:
            self.app.app_params = None

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGeneratorGUI(root)
    root.mainloop()
