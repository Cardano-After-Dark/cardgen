import tkinter as tk

class GuiUtil:
    # ... (existing methods)

    def set_window_size_position(self, window, width, height):
        """
        Sets the window size, minimum size, and centers it on the screen.
        
        :param window: The Tkinter window object
        :param width: Desired width of the window
        :param height: Desired height of the window
        """
        # Set the window size
        window.geometry(f"{width}x{height}")
        
        # Set the minimum size
        window.minsize(width, height)
        
        # Get the screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position for the window to be centered
        position_top = int(screen_height/2 - height/2)
        position_right = int(screen_width/2 - width/2)
        
        # Set the position of the window
        window.geometry(f"+{position_right}+{position_top}")

    # ... (other methods)