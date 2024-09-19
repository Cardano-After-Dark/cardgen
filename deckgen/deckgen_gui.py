import tkinter as tk
import ttkbootstrap as ttk
from tkinter import scrolledtext, filedialog, messagebox
from ttkbootstrap.tooltip import ToolTip
from dataclasses import dataclass, asdict, field
import json
from typing import Dict, Any
import os
from PIL import Image, ImageTk
from deckgen import DeckGen, get_image_module

from deckgen import DeckGen  # Import the DeckGen class we just created

class DeckGenGui:
    def __init__(self, master):
        self.master = master
        self.deckgen = DeckGen()  # Create an instance of DeckGen
        self.preview_window = None  # store preview window reference

        self.style = ttk.Style(theme="cosmo")  # "darkly" or "cosmo"
        master.title("Deck Generator")

        # Set the initial size of the window
        window_width = 500
        window_height = 700
        
        # Get the screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        
        # Calculate the x and y coordinates for the window to be centered
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set the position of the window
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        master.minsize(500, 700)  # Set minimum size

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
                button.grid(row=i, column=2, padx=(5, 0), sticky="w")
                if tooltip:
                    ToolTip(button, text=tooltip)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=0)

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
                button.grid(row=i, column=j+1, padx=(5, 0), sticky="w", pady=2)
                ToolTip(button, text=f"{text.capitalize()} {label.lower()}")
        parent.grid_columnconfigure(0, weight=0)
        parent.grid_columnconfigure(1, weight=0)
        parent.grid_columnconfigure(2, weight=0)
        parent.grid_columnconfigure(3, weight=1)

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
            self.update_deckgen_params()

    def load_parameters(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.deckgen.loadParams(data)
                self.update_gui_from_app()
                self.log("Parameters loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load parameters: {str(e)}")
                self.log(f"Error loading parameters: {str(e)}")

    def save_parameters(self):
        self.update_deckgen_params()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.deckgen.parameters, f, indent=2)
                self.log("Parameters saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save parameters: {str(e)}")
                self.log(f"Error saving parameters: {str(e)}")

    def preview_deck(self):
        try:
            self.update_deckgen_params()
            preview_card = self.deckgen.preview_card()

            # Ensure we're using the correct Image module
            Image = get_image_module()

            # Close the existing preview window if it's open
            if self.preview_window and self.preview_window.winfo_exists():
                self.preview_window.destroy()

            self.preview_window = tk.Toplevel(self.master)
            self.preview_window.title("Deck Preview")
            self.preview_window.geometry("600x500")  # Adjust initial size
            self.preview_window.minsize(600,500)  # Set minimum size

            # Position the preview window next to the main window
            main_x = self.master.winfo_x()
            main_y = self.master.winfo_y()
            main_width = self.master.winfo_width()
            self.preview_window.geometry(f"+{main_x + main_width + 10}+{main_y}")

            # Create a frame to hold the image
            frame = ttk.Frame(self.preview_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Function to resize and display the image
            def resize_image(event):
                # Get the current size of the frame
                width = event.width
                height = event.height

                # Calculate the scaling factor while maintaining aspect ratio
                aspect_ratio = preview_card.width / preview_card.height
                if width / height > aspect_ratio:
                    new_width = int(height * aspect_ratio)
                    new_height = height
                else:
                    new_width = width
                    new_height = int(width / aspect_ratio)

                # Resize the image
                resized_image = preview_card.resize((new_width, new_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)

                # Update the image in the label
                label.config(image=photo)
                label.image = photo  # Keep a reference

            # Create a label to display the image
            label = ttk.Label(frame)
            label.pack(fill=tk.BOTH, expand=True)

            # Bind the resize event
            frame.bind("<Configure>", resize_image)

            self.log(f"[INFO] Deck preview generated for {self.deckgen.parameters['prefix_string']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {str(e)}")
            self.log(f"Error generating preview: {str(e)}")

    def generate_deck(self):
        try:
            self.update_deckgen_params()
            self.deckgen.generate_deck()
            self.log(f"[INFO] Deck generated {self.deckgen.parameters['prefix_string']} into {self.deckgen.parameters['output_folder']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate deck: {str(e)}")
            self.log(f"Error generating deck: {str(e)}")

    def update_gui_from_app(self):
        for attr in ['input_folder', 'output_folder', 'prefix_string']:
            getattr(self, f"{attr}_entry").delete(0, tk.END)
            getattr(self, f"{attr}_entry").insert(0, self.deckgen.parameters[attr])
        self.params_text.delete('1.0', tk.END)
        self.params_text.insert(tk.END, json.dumps(self.deckgen.parameters['app_params'], indent=2))

    def update_deckgen_params(self):
        for attr in ['input_folder', 'output_folder', 'prefix_string']:
            self.deckgen.parameters[attr] = getattr(self, f"{attr}_entry").get()
        try:
            self.deckgen.parameters['app_params'] = json.loads(self.params_text.get('1.0', tk.END))
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON in params section")
        self.deckgen.loadParams(self.deckgen.parameters)

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGenGui(root)
    root.mainloop()