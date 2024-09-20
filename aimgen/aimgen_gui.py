import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os
from aimgen import AIImageGen
from utils.gui_utils import GuiUtil

window_width = 500
window_height = 700

class AIImageGenGUI:
    def __init__(self, master):
        self.master = master
        self.aimgen = AIImageGen()
        self.gui_util = GuiUtil()
        
        self.gui_util.set_window_size_position(master, 800, 600)

        self.style = ttk.Style(theme="darkly")# "darkly" or "cosmo"
        master.title("AI Image Generator")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.create_input_section()
        self.create_action_buttons()
        self.create_persistence_section()
        self.create_image_display()
        
    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.master, text="Generation Parameters", padding=10)
        input_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(input_frame, text="Prompt:").grid(row=0, column=0, sticky='w')
        self.prompt_entry = ttk.Entry(input_frame, width=50)
        self.prompt_entry.grid(row=0, column=1, padx=5, pady=2, sticky='we')
        
        ttk.Label(input_frame, text="Negative Prompt:").grid(row=1, column=0, sticky='w')
        self.negative_prompt_entry = ttk.Entry(input_frame, width=50)
        self.negative_prompt_entry.grid(row=1, column=1, padx=5, pady=2, sticky='we')
        
        ttk.Label(input_frame, text="Aspect Ratio:").grid(row=2, column=0, sticky='w')
        self.aspect_ratio_var = tk.StringVar(value="2:3")
        self.aspect_ratio_combo = ttk.Combobox(input_frame, textvariable=self.aspect_ratio_var, 
                                               values=["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"])
        self.aspect_ratio_combo.grid(row=2, column=1, padx=5, pady=2, sticky='we')
        
        ttk.Label(input_frame, text="Seed:").grid(row=3, column=0, sticky='w')
        self.seed_entry = ttk.Entry(input_frame)
        self.seed_entry.grid(row=3, column=1, padx=5, pady=2, sticky='we')
        self.seed_entry.insert(0, "0")
        
        ttk.Label(input_frame, text="Output Format:").grid(row=4, column=0, sticky='w')
        self.output_format_var = tk.StringVar(value="png")
        self.output_format_combo = ttk.Combobox(input_frame, textvariable=self.output_format_var, 
                                                values=["png", "jpg", "webp"])
        self.output_format_combo.grid(row=4, column=1, padx=5, pady=2, sticky='we')
        
        input_frame.columnconfigure(1, weight=1)
        
    def create_action_buttons(self):
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Reset", command=self.reset_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate", command=self.generate_image).pack(side=tk.LEFT, padx=5)
        
    def create_persistence_section(self):
        persistence_frame = ttk.Frame(self.master)
        persistence_frame.pack(pady=10, fill='x', padx=10)
        
        ttk.Button(persistence_frame, text="Folder", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        self.folder_var = tk.StringVar(value="./out")
        ttk.Entry(persistence_frame, textvariable=self.folder_var, width=30).pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        ttk.Label(persistence_frame, text="Prefix:").pack(side=tk.LEFT, padx=5)
        self.prefix_var = tk.StringVar(value="genio")
        ttk.Entry(persistence_frame, textvariable=self.prefix_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(persistence_frame, text="Save", command=self.save_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(persistence_frame, text="Load", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
    def create_image_display(self):
        self.image_frame = ttk.LabelFrame(self.master, text="Generated Image", padding=10)
        self.image_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True, fill='both')
        
    def reset_fields(self):
        self.prompt_entry.delete(0, tk.END)
        self.negative_prompt_entry.delete(0, tk.END)
        self.aspect_ratio_var.set("2:3")
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, "0")
        self.output_format_var.set("png")
        
    def generate_image(self):
        self.aimgen.set_parameters(
            prompt=self.prompt_entry.get(),
            negative_prompt=self.negative_prompt_entry.get(),
            aspect_ratio=self.aspect_ratio_var.get(),
            seed=int(self.seed_entry.get()),
            output_format=self.output_format_var.get()
        )
        
        image, result = self.aimgen.generate_image()
        self.display_image(image)
        
    def display_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            
    def save_image(self):
        filename = self.aimgen.save_image(self.folder_var.get(), self.prefix_var.get())
        if filename:
            print(f"Image saved as {filename}")
        
    def load_image(self):
        filename = filedialog.askopenfilename(initialdir=self.folder_var.get(), 
                                              filetypes=[("Image files", "*.png;*.jpg;*.webp")])
        if filename:
            image = self.aimgen.load_image(filename)
            self.display_image(image)
            print(f"Image loaded from {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIImageGenGUI(root)
    root.mainloop()
