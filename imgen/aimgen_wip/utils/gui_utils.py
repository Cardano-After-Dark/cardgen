import tkinter as tk
from PIL import Image, ImageTk

class GuiUtil:
    @staticmethod
    def set_window_size(window, width, height):
        """
        Sets the window size and minimum size.
        
        :param window: The Tkinter window object
        :param width: Desired width of the window
        :param height: Desired height of the window
        """
        window.geometry(f"{width}x{height}")
        window.minsize(width, height)

    @staticmethod
    def center_window(window, width, height):
        """
        Centers the window on the screen and sets its size.
        
        :param window: The Tkinter window object
        :param width: Desired width of the window
        :param height: Desired height of the window
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = int(screen_width/2 - width/2)
        y = int(screen_height/2 - height/2)
        
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.minsize(width, height)

    @staticmethod
    def position_window(window, width, height, reference_window=None, position='top_left'):
        """
        Positions the window relative to a reference window or at the top-left of the screen.
        
        :param window: The Tkinter window object to position
        :param width: Desired width of the window
        :param height: Desired height of the window
        :param reference_window: The reference Tkinter window object (optional)
        :param position: The position relative to the reference window ('top_left', 'top_right', 'bottom_left', 'bottom_right')
        """
        if reference_window:
            ref_x = reference_window.winfo_x()
            ref_y = reference_window.winfo_y()
            ref_width = reference_window.winfo_width()
            ref_height = reference_window.winfo_height()

            if position == 'top_left':
                x, y = ref_x, ref_y
            elif position == 'top_right':
                x, y = ref_x + ref_width, ref_y
            elif position == 'bottom_left':
                x, y = ref_x, ref_y + ref_height
            elif position == 'bottom_right':
                x, y = ref_x + ref_width, ref_y + ref_height
            else:
                x, y = ref_x, ref_y  # Default to top_left if invalid position is given
        else:
            x, y = 0, 0  # Position at top-left of the screen if no reference window is provided

        window.geometry(f"{width}x{height}+{x}+{y}")
        window.minsize(width, height)

    @staticmethod
    def bring_window_to_front(window):
        """
        Brings the specified window to the front and gives it focus.
        
        :param window: The Tkinter window object
        """
        window.lift()
        window.focus_set()

    @staticmethod
    def resize_image_for_window(image, window, max_width=None, max_height=None):
        """
        Resizes an image to fit within the given window dimensions while maintaining aspect ratio.
        
        :param image: PIL Image object
        :param window: Tkinter window or widget object
        :param max_width: Maximum width for the image (optional)
        :param max_height: Maximum height for the image (optional)
        :return: PhotoImage object of the resized image
        """
        # Get the current size of the window or widget
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        # Use provided max dimensions if available, otherwise use window dimensions
        max_width = max_width or window_width
        max_height = max_height or window_height

        # If both dimensions are 0, return the original image
        if max_width == 0 and max_height == 0:
            return ImageTk.PhotoImage(image)

        # Get the original image dimensions
        img_width, img_height = image.size

        # Calculate the scaling factor
        width_ratio = max_width / img_width if max_width > 0 else 1
        height_ratio = max_height / img_height if max_height > 0 else 1
        scale_factor = min(width_ratio, height_ratio)

        # Calculate new dimensions
        new_width = max(1, int(img_width * scale_factor))
        new_height = max(1, int(img_height * scale_factor))

        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)

        # Convert to PhotoImage
        return ImageTk.PhotoImage(resized_image)