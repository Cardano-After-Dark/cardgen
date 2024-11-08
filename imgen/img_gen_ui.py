import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import time

class ImgGenUI:
    def __init__(self, master, gen_io, on_generate, on_save, on_load):
        self.master = master
        self.gen_io = gen_io
        self.on_generate = on_generate
        self.on_save = on_save
        self.on_load = on_load

        self.create_widgets()
        self.update_fields(gen_io)

    def create_widgets(self):
        self.create_header()
        self.create_input_fields()
        self.create_action_buttons()
        self.create_persistence_controls()
        self.create_image_display()

    def create_header(self):
        ttk.Label(self.master, text="Stability.ai generation with Stable Image Core").pack(pady=10)

    def create_input_fields(self):
        input_frame = ttk.Frame(self.master)
        input_frame.pack(pady=10)

        self.prompt_entry = self.create_labeled_entry(input_frame, "Prompt:", 0, width=80)
        self.negative_prompt_entry = self.create_labeled_entry(input_frame, "Negative Prompt:", 1, width=80)
        self.aspect_ratio_var, self.aspect_ratio_combo = self.create_labeled_combobox(
            input_frame, "Aspect Ratio:", 2, 
            values=["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21", "5:7"]
        )
        self.seed_entry = self.create_labeled_entry(input_frame, "Seed:", 3)
        self.output_format_var, self.output_format_combo = self.create_labeled_combobox(
            input_frame, "Output Format:", 4, 
            values=["webp", "jpeg", "png"]
        )

    def create_action_buttons(self):
        action_frame = ttk.Frame(self.master)
        action_frame.pack(pady=10)
        ttk.Button(action_frame, text="Reset", command=self.reset_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Generate", command=self.generate).pack(side=tk.LEFT, padx=5)

    def create_persistence_controls(self):
        persistence_frame = ttk.Frame(self.master)
        persistence_frame.pack(pady=10)

        self.folder_var = tk.StringVar(value="./out")
        ttk.Button(persistence_frame, text="Folder", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        ttk.Entry(persistence_frame, textvariable=self.folder_var, width=30).pack(side=tk.LEFT, padx=5)

        self.prefix_var = tk.StringVar(value="genio")
        ttk.Label(persistence_frame, text="Prefix:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(persistence_frame, textvariable=self.prefix_var, width=20).pack(side=tk.LEFT, padx=5)

        ttk.Button(persistence_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(persistence_frame, text="Load", command=self.load).pack(side=tk.LEFT, padx=5)

    def create_image_display(self):
        self.image_frame = ttk.Frame(self.master)
        self.image_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        self.master.bind('<Configure>', self.schedule_resize)
        self.image_handler = ImageHandler(self.image_frame, self.image_label)

    def create_labeled_entry(self, parent, label, row, **kwargs):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e")
        entry = ttk.Entry(parent, **kwargs)
        entry.grid(row=row, column=1, padx=5)
        return entry

    def create_labeled_combobox(self, parent, label, row, values):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e")
        var = tk.StringVar()
        combo = ttk.Combobox(parent, textvariable=var, values=values)
        combo.grid(row=row, column=1, padx=5)
        return var, combo

    def reset_fields(self):
        self.prompt_entry.delete(0, tk.END)
        self.negative_prompt_entry.delete(0, tk.END)
        self.aspect_ratio_var.set("2:3")
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, "0")
        self.output_format_var.set("png")

    def generate(self):
        self.gen_io.prompt = self.prompt_entry.get()
        self.gen_io.negative_prompt = self.negative_prompt_entry.get()
        self.gen_io.aspect_ratio = self.aspect_ratio_var.get()
        self.gen_io.seed = int(self.seed_entry.get())
        self.gen_io.output_format = self.output_format_var.get()
        
        self.on_generate(self.gen_io)
        self.image_handler.update_image(self.gen_io.gen_image)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def save(self):
        self.on_save(self.folder_var.get(), self.prefix_var.get())

    def load(self):
        self.gen_io = self.on_load(self.folder_var.get(), self.prefix_var.get())
        self.update_fields(self.gen_io)
        self.image_handler.update_image(self.gen_io.gen_image)

    def update_fields(self, gen_io):
        self.prompt_entry.delete(0, tk.END)
        self.prompt_entry.insert(0, gen_io.prompt)
        self.negative_prompt_entry.delete(0, tk.END)
        self.negative_prompt_entry.insert(0, gen_io.negative_prompt)
        self.aspect_ratio_var.set(gen_io.aspect_ratio)
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, str(gen_io.seed))
        self.output_format_var.set(gen_io.output_format)
        self.image_handler.update_image(gen_io.gen_image)

    def schedule_resize(self, event=None):
        self.image_handler.schedule_resize()

class ImageHandler:
    def __init__(self, frame, label):
        self.frame = frame
        self.label = label
        self.original_image = None
        self.photo = None
        self.last_resize_time = 0
        self.resize_delay = 200  # milliseconds

    def update_image(self, image=None):
        if image:
            self.original_image = image
            self.resize_image(force=True)
        else:
            self.original_image = None
            self.photo = None
            self.label.config(image=None)

    def schedule_resize(self):
        current_time = time.time() * 1000
        if current_time - self.last_resize_time > self.resize_delay:
            self.last_resize_time = current_time
            self.frame.after(self.resize_delay, self.resize_image)

    def resize_image(self, force=False):
        if self.original_image:
            frame_width = self.frame.winfo_width()
            frame_height = self.frame.winfo_height()

            if frame_width > 1 and frame_height > 1:
                img_width, img_height = self.original_image.size
                scale = min(frame_width/img_width, frame_height/img_height)
                
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)

                if force or abs(new_width - getattr(self, 'last_width', 0)) > 10 or abs(new_height - getattr(self, 'last_height', 0)) > 10:
                    self.last_width, self.last_height = new_width, new_height

                    resized_image = self.original_image.copy()
                    resized_image = resized_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    self.photo = ImageTk.PhotoImage(resized_image)
                    self.label.config(image=self.photo)
                    self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)