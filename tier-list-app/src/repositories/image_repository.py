import io
import secrets
import os
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, UnidentifiedImageError


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

        Raises:
            UnidentifiedImageError:
                Error, when the format of the file/image not supported
            FileNotFoundError:
                Error, when image missing from data/images/
        """

        try:
            img = Image.open(file_path)
            img = img.resize((100, 100))
            return ImageTk.PhotoImage(img)

        except UnidentifiedImageError as e:
            raise ValueError(
                f'Format of {os.path.basename(file_path)} not supported') from e

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f'Image {os.path.basename(file_path)} missing from data/images/') from e

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

        target_dir = Path('services/../data/images/').resolve()
        base_dir = Path('services/../').resolve()

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

    @staticmethod
    def take_canvas_screenshot(canvas):
        """Creates a screenshot of the whole tier list.
        Image is given a random name and saved to data/screenshots/.

        Args:
            canvas: TkInter canvas-object.

        Returns:
            Image name for confirmation.
        """

        data = canvas.postscript(colormode='color',
                                 x=0, y=0,
                                 width=canvas.bbox("all")[2],
                                 height=canvas.bbox("all")[3],
                                 pagewidth=canvas.bbox("all")[2],
                                 pageheight=canvas.bbox("all")[3])

        image = Image.open(io.BytesIO(data.encode('utf-8')))
        image = ImageOps.expand(image, border=2, fill='white')

        target_dir = Path('services/../data/screenshots').resolve()

        image_name = 'screenshot_' + f'{secrets.token_hex(8)}.png'
        target_path = target_dir / image_name

        image.save(target_path)

        return image_name


image_repository = ImageRepository()
