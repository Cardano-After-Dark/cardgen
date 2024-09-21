import tkinter as tk
from tkinter import filedialog, scrolledtext
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os
from aimgen import AIImageGen
from utils.gui_utils import GuiUtil

class AIImageGenGUI:
    def __init__(self, master):
        self.master = master
        self.aimgen = AIImageGen()
        
        GuiUtil.center_window(master, 800, 600)

        self.style = ttk.Style(theme="darkly")
        master.title("AI Image Generator")
        
        self.create_widgets()
        self.preview_window = None
        self.preview_image = None
        
    def create_widgets(self):
        self.create_input_section()
        self.create_action_buttons()
        self.create_persistence_section()
        self.create_log_section()
        
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

    def create_log_section(self):
        log_frame = ttk.LabelFrame(self.master, text="Log", padding=10)
        log_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(fill='both', expand=True)

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    # def create_image_display(self):
    #     self.image_frame = ttk.LabelFrame(self.master, text="Generated Image", padding=10)
    #     self.image_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
    #     self.image_label = ttk.Label(self.image_frame)
    #     self.image_label.pack(expand=True, fill='both')
        
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
        self.log(f"Image generated: {result}")
        self.show_preview(image)

    def show_preview(self, image):
        # Close the existing preview window if it's open
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()

        self.preview_window = tk.Toplevel(self.master)
        self.preview_window.title("Image Preview")
        self.preview_window.geometry("600x700")  # Adjust initial size
        self.preview_window.minsize(600, 700)  # Set minimum size

        # Position the preview window to the right of the main window
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        self.preview_window.geometry(f"+{main_x + main_width + 10}+{main_y}")

        # Create a frame to hold the image
        frame = ttk.Frame(self.preview_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create a label to display the image
        self.preview_label = ttk.Label(frame)
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Save button
        save_button = ttk.Button(self.preview_window, text="Save", command=self.save_preview_image)
        save_button.pack(pady=10)

        # Store the original image
        self.preview_image = image

        # Function to resize and display the image
        def resize_image(event=None):
            if self.preview_image:
                # Get the current size of the frame
                width = frame.winfo_width()
                height = frame.winfo_height()

                # Calculate the scaling factor while maintaining aspect ratio
                img_width, img_height = self.preview_image.size
                aspect_ratio = img_width / img_height
                if width / height > aspect_ratio:
                    new_width = int(height * aspect_ratio)
                    new_height = height
                else:
                    new_width = width
                    new_height = int(width / aspect_ratio)

                # Resize the image
                resized_image = self.preview_image.resize((new_width, new_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)

                # Update the image in the label
                self.preview_label.config(image=photo)
                self.preview_label.image = photo  # Keep a reference

        # Bind the resize event
        frame.bind("<Configure>", resize_image)

        # Initial resize
        self.preview_window.update()
        resize_image()

    def save_preview_image(self):
        if self.preview_image:
            filename = self.aimgen.save_image(self.folder_var.get(), self.prefix_var.get())
            if filename:
                self.log(f"Image saved as {filename}")
            else:
                self.log("Failed to save image")
        else:
            self.log("No image to save")


    # def display_image(self, image):
    #     photo = ImageTk.PhotoImage(image)
    #     self.image_label.config(image=photo)
    #     self.image_label.image = photo
        
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
