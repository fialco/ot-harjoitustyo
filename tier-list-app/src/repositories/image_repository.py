import os
from PIL import Image, ImageTk


class ImageRepository:
    @staticmethod
    def load_image(file_path):
        """Load and resize image from file path."""
        img = Image.open(file_path)
        img = img.resize((100, 100))
        return ImageTk.PhotoImage(img)

    @staticmethod
    def get_base_dir_path():
        """Returns full path to base dir."""
        current_dir = os.path.dirname(__file__)
        return os.path.dirname(os.path.dirname(current_dir))
