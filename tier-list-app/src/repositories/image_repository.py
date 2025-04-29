from pathlib import Path
from PIL import Image, ImageTk


class ImageRepository:
    """Class, which handles operations for images and their paths.
    """

    @staticmethod
    def load_image(file_path):
        """Load and resize an image.

        Args:
            file_path: String of an absolute path to image.

        Returns:
            A PhotoImage-object.
        """

        img = Image.open(file_path)
        img = img.resize((100, 100))
        return ImageTk.PhotoImage(img)

    @staticmethod
    def get_base_dir_path():
        """Get the absolute path to base directory.
        E.g. '/home/user/ot-harjoitustyo/tier-list-app'.

        Returns:
            String of an absolute path to base directory.
        """
        return str(Path(__file__).resolve().parent.parent.parent)

    @staticmethod
    def check_image_paths(image_paths):
        """Checks if image in /data/images/.
        If not then make a small copy there and that path is saved.

        Args:
            file_path: List of absolute paths to images.

        Returns:
            List of relative image paths in data/images/ directory.
        """

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


image_repository = ImageRepository()
