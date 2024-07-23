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

        # Image display
        self.original_image = None
        self.photo = None
        self.last_resize_time = 0
        self.resize_delay = 200  # milliseconds

        self.create_widgets()
        self.update_fields(gen_io)  # Initialize fields with current gen_io state

    def create_widgets(self):
        # Row 1: Header
        ttk.Label(self.master, text="Stability.ai generation with Stable Image Core").pack(pady=10)

        # Row 2: Input fields
        input_frame = ttk.Frame(self.master)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Prompt:").grid(row=0, column=0, sticky="e")
        self.prompt_entry = ttk.Entry(input_frame, width=80)
        self.prompt_entry.grid(row=0, column=1, padx=5)
        self.prompt_entry.insert(0, self.gen_io.prompt)

        ttk.Label(input_frame, text="Negative Prompt:").grid(row=1, column=0, sticky="e")
        self.negative_prompt_entry = ttk.Entry(input_frame, width=80)
        self.negative_prompt_entry.grid(row=1, column=1, padx=5)
        self.negative_prompt_entry.insert(0, self.gen_io.negative_prompt)

        ttk.Label(input_frame, text="Aspect Ratio:").grid(row=2, column=0, sticky="e")
        self.aspect_ratio_var = tk.StringVar(value=self.gen_io.aspect_ratio)
        self.aspect_ratio_combo = ttk.Combobox(input_frame, textvariable=self.aspect_ratio_var, 
                                               values=["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"])
        self.aspect_ratio_combo.grid(row=2, column=1, padx=5)

        ttk.Label(input_frame, text="Seed:").grid(row=3, column=0, sticky="e")
        self.seed_entry = ttk.Entry(input_frame)
        self.seed_entry.grid(row=3, column=1, padx=5)
        self.seed_entry.insert(0, str(self.gen_io.seed))

        ttk.Label(input_frame, text="Output Format:").grid(row=4, column=0, sticky="e")
        self.output_format_var = tk.StringVar(value=self.gen_io.output_format)
        self.output_format_combo = ttk.Combobox(input_frame, textvariable=self.output_format_var, 
                                                values=["webp", "jpeg", "png"])
        self.output_format_combo.grid(row=4, column=1, padx=5)

        # Row 3: Action buttons
        action_frame = ttk.Frame(self.master)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Reset", command=self.reset_fields).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Generate", command=self.generate).pack(side=tk.LEFT, padx=5)

        # Row 4: Persistence
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

        # Row 5: Output image
        self.image_frame = ttk.Frame(self.master)
        self.image_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Resize the image on scheduling to avoid performance issues
        self.master.bind('<Configure>', self.schedule_resize)

        self.update_image()

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
        self.update_image()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def save(self):
        folder = self.folder_var.get()
        prefix = self.prefix_var.get()
        self.on_save(folder, prefix)

    def load(self):
        folder = self.folder_var.get()
        prefix = self.prefix_var.get()
        self.gen_io = self.on_load(folder, prefix)
        self.update_fields()
        self.update_image()

    def update_fields(self, gen_io):
        self.prompt_entry.delete(0, tk.END)
        self.prompt_entry.insert(0, gen_io.prompt)
        self.negative_prompt_entry.delete(0, tk.END)
        self.negative_prompt_entry.insert(0, gen_io.negative_prompt)
        self.aspect_ratio_var.set(gen_io.aspect_ratio)
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, str(gen_io.seed))
        self.output_format_var.set(gen_io.output_format)
        self.update_image(gen_io.gen_image)

    def update_image(self, image=None):
        if image:
            self.original_image = image
            self.resize_image(force=True)
        else:
            self.original_image = None
            self.photo = None
            self.image_label.config(image=None)

    def schedule_resize(self, event=None):
        current_time = time.time() * 1000
        if current_time - self.last_resize_time > self.resize_delay:
            self.last_resize_time = current_time
            self.master.after(self.resize_delay, self.resize_image)

    def resize_image(self, force=False):
        if self.original_image:
            # Get the current size of the frame
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            if frame_width > 1 and frame_height > 1:  # Ensure valid dimensions
                # Calculate the scaling factor to fit the image within the frame
                img_width, img_height = self.original_image.size
                scale = min(frame_width/img_width, frame_height/img_height)
                
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)

                # Only resize if the size has changed significantly or forced
                if force or abs(new_width - getattr(self, 'last_width', 0)) > 10 or abs(new_height - getattr(self, 'last_height', 0)) > 10:
                    self.last_width, self.last_height = new_width, new_height

                    # Resize the image
                    resized_image = self.original_image.copy()
                    resized_image = resized_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # Create a new PhotoImage object
                    self.photo = ImageTk.PhotoImage(resized_image)

                    # Update the label with the new image
                    self.image_label.config(image=self.photo)
                    
                    # Center the image
                    self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
