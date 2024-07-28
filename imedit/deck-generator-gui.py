import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class DeckGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Deck Generator")
        master.geometry("400x600")

        # Create main frame
        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # Generation Section
        self.create_generation_section(main_frame)

        # Design Section
        self.create_design_section(main_frame)

        # Actions Section
        self.create_actions_section(main_frame)

        # Log Section
        self.create_log_section(main_frame)

    def create_generation_section(self, parent):
        generation_frame = ttk.LabelFrame(parent, text="Generation", padding="10")
        generation_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        parent.columnconfigure(0, weight=1)

        # Input folder
        ttk.Label(generation_frame, text="Input folder:").grid(row=0, column=0, sticky=tk.W)
        input_entry = ttk.Entry(generation_frame)
        input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(generation_frame, text="select").grid(row=0, column=2, padx=(5, 0))

        # Output folder
        ttk.Label(generation_frame, text="Output folder:").grid(row=1, column=0, sticky=tk.W)
        output_entry = ttk.Entry(generation_frame)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Button(generation_frame, text="select").grid(row=1, column=2, padx=(5, 0))

        # Prefix string
        ttk.Label(generation_frame, text="Prefix string:").grid(row=2, column=0, sticky=tk.W)
        prefix_entry = ttk.Entry(generation_frame)
        prefix_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

        generation_frame.columnconfigure(1, weight=1)

    def create_design_section(self, parent):
        design_frame = ttk.LabelFrame(parent, text="Design", padding="10")
        design_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        parent.rowconfigure(1, weight=1)

        design_text = scrolledtext.ScrolledText(design_frame, wrap=tk.WORD, height=10)
        design_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        design_frame.columnconfigure(0, weight=1)
        design_frame.rowconfigure(0, weight=1)

    def create_actions_section(self, parent):
        actions_frame = ttk.LabelFrame(parent, text="Actions", padding="10")
        actions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(actions_frame, text="Parameters").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(actions_frame, text="load", style="TButton").grid(row=0, column=1, padx=(5, 0))
        ttk.Button(actions_frame, text="save", style="TButton").grid(row=0, column=2, padx=(5, 0))

        ttk.Label(actions_frame, text="Deck").grid(row=1, column=0, sticky=tk.W)
        ttk.Button(actions_frame, text="preview", style="TButton").grid(row=1, column=1, padx=(5, 0))
        ttk.Button(actions_frame, text="generate", style="TButton").grid(row=1, column=2, padx=(5, 0))

    def create_log_section(self, parent):
        log_frame = ttk.LabelFrame(parent, text="Log", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        parent.rowconfigure(3, weight=1)

        log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckGeneratorGUI(root)
    root.mainloop()
