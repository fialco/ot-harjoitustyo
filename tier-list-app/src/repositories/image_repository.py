from PIL import Image, ImageTk


class ImageRepository:
    @staticmethod
    def load_image(file_path):
        """Load and resize image from file path."""
        img = Image.open(file_path)
        img = img.resize((100, 100))
        return ImageTk.PhotoImage(img)
