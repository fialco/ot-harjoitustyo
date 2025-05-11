import io
import secrets
import os
import textwrap
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError


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
            image = Image.open(file_path)
            image = image.resize((100, 100))
            return ImageTk.PhotoImage(image)

        except UnidentifiedImageError as e:
            raise ValueError(
                f'Format of {os.path.basename(file_path)} not supported') from e

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f'Image {os.path.basename(file_path)} missing from data/images/') from e

    @staticmethod
    def text_to_image(text):
        """Creates an image from the text given.

        Args:
            text: Value to be made an image.

        Returns:
            A PhotoImage-object.
        """

        image = Image.new('RGB', (100, 100), color='black')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("FreeSansBold.otf", 15)
        except IOError:
            font = ImageFont.load_default()

        # Asked ChatGPT to write code for wrapping long text
        max_chars_per_line = 10
        lines = textwrap.wrap(text, width=max_chars_per_line)

        line_height = font.getbbox('A')[3] - font.getbbox('A')[1] + 2
        total_text_height = line_height * len(lines)

        y = (100 - total_text_height) // 2

        for line in lines:
            line_width = draw.textlength(line, font=font)
            x = (100 - line_width) // 2
            draw.text((x, y), line, fill='white', font=font)
            y += line_height
        # Generated code ends

        target_dir = Path('services/../data/images').resolve()

        image_name = f'{text}_{secrets.token_hex(8)}.png'
        target_path = target_dir / image_name

        image.save(target_path)

        return ImageTk.PhotoImage(image), target_path

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
