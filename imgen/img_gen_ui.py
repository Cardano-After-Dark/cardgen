# imgen/img_gen_ui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

class ImgGenUI:
    def __init__(self, master, gen_io, on_generate, on_save, on_load):
        self.master = master
        self.gen_io = gen_io
        self.on_generate = on_generate
        self.on_save = on_save
        self.on_load = on_load

        self.folder = './out'
        self.prefix = 'latest_genio'

        self.build_ui()

    def build_ui(self):
        self.master.title("Stability.ai generation with Stable Image Core")

        # Header
        header = tk.Label(self.master, text="Stability.ai generation with Stable Image Core", font=("Arial", 16))
        header.pack(pady=10)

        # Input grid
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Prompt:").grid(row=0, column=0, sticky="e")
        self.prompt_entry = tk.Entry(input_frame, width=50)
        self.prompt_entry.grid(row=0, column=1, padx=10)

        tk.Label(input_frame, text="Negative Prompt:").grid(row=1, column=0, sticky="e")
        self.negative_prompt_entry = tk.Entry(input_frame, width=50)
        self.negative_prompt_entry.grid(row=1, column=1, padx=10)

        tk.Label(input_frame, text="Aspect Ratio:").grid(row=2, column=0, sticky="e")
        self.aspect_ratio_var = tk.StringVar(value="2:3")
        self.aspect_ratio_dropdown = tk.OptionMenu(input_frame, self.aspect_ratio_var, "21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21")
        self.aspect_ratio_dropdown.grid(row=2, column=1, padx=10)

        tk.Label(input_frame, text="Seed:").grid(row=3, column=0, sticky="e")
        self.seed_entry = tk.Entry(input_frame, width=10)
        self.seed_entry.grid(row=3, column=1, padx=10, sticky="w")

        tk.Label(input_frame, text="Output Format:").grid(row=4, column=0, sticky="e")
        self.output_format_var = tk.StringVar(value="png")
        self.output_format_dropdown = tk.OptionMenu(input_frame, self.output_format_var, "webp", "jpeg", "png")
        self.output_format_dropdown.grid(row=4, column=1, padx=10)

        # UI actions
        action_frame = tk.Frame(self.master)
        action_frame.pack(pady=10)

        reset_button = tk.Button(action_frame, text="Reset", command=self.reset_inputs)
        reset_button.grid(row=0, column=0, padx=10)

        generate_button = tk.Button(action_frame, text="Generate", command=self.generate_image)
        generate_button.grid(row=0, column=1, padx=10)

        # Persistence
        persistence_frame = tk.Frame(self.master)
        persistence_frame.pack(pady=10)

        folder_button = tk.Button(persistence_frame, text="Folder", command=self.select_folder)
        folder_button.grid(row=0, column=0, padx=10)

        self.prefix_entry = tk.Entry(persistence_frame, width=20)
        self.prefix_entry.insert(0, self.prefix)
        self.prefix_entry.grid(row=0, column=1, padx=10)

        save_button = tk.Button(persistence_frame, text="Save", command=self.save_data)
        save_button.grid(row=0, column=2, padx=10)

        load_button = tk.Button(persistence_frame, text="Load", command=self.load_data)
        load_button.grid(row=0, column=3, padx=10)

        # Output
        self.output_label = tk.Label(self.master, text="Result image:")
        self.output_label.pack(pady=10)

        self.output_image_label = tk.Label(self.master)
        self.output_image_label.pack(pady=10)

    def reset_inputs(self):
        self.prompt_entry.delete(0, tk.END)
        self.negative_prompt_entry.delete(0, tk.END)
        self.aspect_ratio_var.set("2:3")
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, "0")
        self.output_format_var.set("png")

    def generate_image(self):
        self.gen_io.prompt = self.prompt_entry.get()
        self.gen_io.negative_prompt = self.negative_prompt_entry.get()
        self.gen_io.aspect_ratio = self.aspect_ratio_var.get()
        self.gen_io.seed = int(self.seed_entry.get())
        self.gen_io.output_format = self.output_format_var.get()

        self.on_generate(self.gen_io)

    def select_folder(self):
        self.folder = filedialog.askdirectory(initialdir="./out")
        if not self.folder:
            self.folder = './out'

    def save_data(self):
        self.prefix = self.prefix_entry.get()
        if not self.prefix:
            messagebox.showwarning("Warning", "Prefix cannot be empty")
            return

        self.on_save(self.folder, self.prefix)

    def load_data(self):
        self.prefix = self.prefix_entry.get()
        if not self.prefix:
            messagebox.showwarning("Warning", "Prefix cannot be empty")
            return

        self.on_load(self.folder, self.prefix)

    def display_image(self, image):
        img = ImageTk.PhotoImage(image)
        self.output_image_label.config(image=img)
        self.output_image_label.image = img
