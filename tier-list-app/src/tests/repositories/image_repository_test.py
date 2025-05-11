import unittest
from PIL import ImageTk
from tkinterdnd2 import TkinterDnD
from repositories.image_repository import image_repository


class TestImageRepository(unittest.TestCase):
    def setUp(self):
        base_path = image_repository.get_base_dir_path()
        self.test_image_1_path = base_path + '/data/test_images/test_image_1.jpg'
        self.test_text_path = base_path + '/data/test_images/test_file.txt'
        self.test_missing_path = base_path + '/data/test_images/missing.png'

    def test_get_correct_base_dir_path(self):
        wanted_path = 'ot-harjoitustyo/tier-list-app'
        base_path = image_repository.get_base_dir_path()

        self.assertIn(wanted_path, base_path)

    def test_load_valid_image(self):
        """ For PIL to work Tk() window must be running
        """
        root = TkinterDnD.Tk()
        root.withdraw()

        image = image_repository.load_image(self.test_image_1_path)

        self.assertIsInstance(image, ImageTk.PhotoImage)
        self.assertEqual(image.height(), 100)

        root.destroy()

    def test_load_file_with_invalid_format(self):
        """ Testing raises:
        https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaisesRegex
        """
        root = TkinterDnD.Tk()
        root.withdraw()

        with self.assertRaisesRegex(ValueError, 'Format of test_file.txt not supported'):
            image_repository.load_image(self.test_text_path)

        root.destroy()

    def test_load_missing_file(self):
        root = TkinterDnD.Tk()
        root.withdraw()

        with self.assertRaisesRegex(FileNotFoundError, 'Image missing.png missing from data/images/'):
            image_repository.load_image(self.test_missing_path)

        root.destroy()

    def test_text_to_image(self):
        root = TkinterDnD.Tk()
        root.withdraw()

        image, target_path = image_repository.text_to_image('testing')

        self.assertIsInstance(image, ImageTk.PhotoImage)
        self.assertEqual(image.height(), 100)

        root.destroy()

