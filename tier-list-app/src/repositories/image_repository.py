from pathlib import Path
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
        return str(Path(__file__).resolve().parent.parent.parent)

    @staticmethod
    def check_image_paths(image_paths):
        """Checks if image in /data/images/.
        If not then make a small copy there and that path is saved."""

        target_dir = Path("services/../data/images/").resolve()
        base_dir = Path("services/../").resolve()

        new_paths = []

        for path in image_paths:
            image_path = Path(path).resolve()

            if target_dir not in image_path.parents:
                target_path = target_dir / image_path.name

                img = Image.open(image_path)
                img = img.resize((200, 200))
                img.save(target_path)

                relative_path = target_path.relative_to(base_dir)
                new_paths.append("/" + str(relative_path))

            else:
                relative_path = image_path.relative_to(base_dir)
                new_paths.append("/" + str(relative_path))

        return new_paths
