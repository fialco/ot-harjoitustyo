class ImageItem:
    def __init__(self, image, item_id, x, y):
        self.image = image
        self.item_id = item_id
        self.x = x
        self.y = y

    def update_position(self, x, y):
        self.x = x
        self.y = y
