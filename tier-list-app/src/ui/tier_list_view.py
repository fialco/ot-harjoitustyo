import tkinter as tk
from tkinter import ttk, simpledialog
from tkinterdnd2 import TkinterDnD, DND_FILES

from services.tier_list_service import TierListService
from repositories.image_repository import ImageRepository


class TierListView:
    def __init__(self, root, handle_show_list_view, tierlist_id):
        self._root = root

        self._item_service = ItemHandler()

        self._tier_list_service = TierListService()

        self._handle_show_list_view = handle_show_list_view

        self._tierlist_id = tierlist_id

        self.frame = tk.Frame(self._root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for items and tiers
        self._canvas = tk.Canvas(self.frame, bg="snow2", height=900, width=800)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tier_height = 100

        self._init_tier_list_data()

        # Draw tiers on the canvas
        self._draw_tiers()

        # Dictionary to store item ID to ImageItem mapping
        # Proper storage later
        self._item_map = {}

        self._create_drag_drop_area()

        self._draw_items()

        self._create_back_button()
        self._create_create_button()

        scrollbar = ttk.Scrollbar(self.frame, command=self._canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Config canvast to use the scrollbar
        self._canvas.config(yscrollcommand=scrollbar.set)

        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def pack(self):
        """Show view."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """Destory view."""
        self.frame.destroy()

    def tier_list_name_input(self):
        if not self._tierlist_id:
            name = simpledialog.askstring(
                title="Tier list name", prompt="Name the tier list:", parent=self._root)
            self._canvas.itemconfig(self.canvas_tier_list_name, text=name)

            self._tier_list_name = name

    def _init_tier_list_data(self):
        self._tier_list_name = 'Click here to name the tier list'

        # Default tiers
        self._tiers = {0: 'S', 1: 'A', 2: 'B', 3: 'C', 4: 'D'}

        if self._tierlist_id:
            tier_list = self._tier_list_service.get_tier_list(
                self._tierlist_id)
            self._tier_list_name = tier_list.name

            tier_data = self._tier_list_service.get_tiers_of_tier_list(
                self._tierlist_id)

            self._tiers = {}
            for tier in tier_data:
                self._tiers[tier.rank] = tier.name

        self.tier_positions = [(i+1)*100 for i in range(len(self._tiers))]
        self.tier_positions.append((len(self._tiers)+1)*100)
        self._tier_count = (len(self._tiers)+1)*100

    def _draw_tiers(self):
        """Draw the tiers on the canvas."""
        self._canvas.create_rectangle(0, 0, 800, 75,
                                      outline='black', width=2, fill='SpringGreen2')

        self.canvas_tier_list_name = self._canvas.create_text(
            400, 25, text=f"{self._tier_list_name}", font=('Arial', 25, 'bold'), fill='blue')

        self._canvas.tag_bind(
            self.canvas_tier_list_name, '<Button-1>', lambda e: self.tier_list_name_input())

        # Adds the amount of tiers given
        for rank, tier in self._tiers.items():
            self._canvas.create_rectangle(0, self.tier_positions[rank] - self.tier_height // 2,
                                          800, self.tier_positions[rank] +
                                          self.tier_height // 2,
                                          outline='black', width=2, fill='azure')

            self._canvas.create_text(10, self.tier_positions[rank], anchor='w', text=f"[{tier}]",
                                     font=('Arial', 35, 'bold'))

        # Add container for unpicked items
        self._canvas.create_rectangle(0, self._tier_count - self.tier_height // 2,
                                      800, self._tier_count +
                                      self.tier_height // 2,
                                      outline='black', width=2, fill='gray80')

    def _draw_items(self):
        items = self._tier_list_service.get_items_of_tier_list(
            self._tierlist_id)

        base_dir = self._tier_list_service.get_base_dir_path()

        for i, item in enumerate(items):
            # Position where the items will be placed
            x, y = (i + 1) * 120, self._tier_count

            image_path = base_dir + item.image_path

            # Add the image item
            image_item = self._item_service.add_item(image_path, x, y)

            # Place the image on the canvas
            item_id = self._canvas.create_image(x, y, image=image_item.image)
            self._canvas.image = image_item.image

            # Store the image_item
            self._item_map[item_id] = image_item

            # Bind drag movement event
            self._canvas.tag_bind(item_id, '<B1-Motion>', lambda e,
                                  id=item_id: self._on_drag(e, id))
            self._canvas.tag_bind(
                item_id, '<ButtonRelease-1>', self._on_drop_item)

    # Change dropzone color with mouse hover

    def _on_hover(self, event):
        self.drop_label.config(bg='yellow')

    def _on_leave(self, event):
        self.drop_label.config(bg='green')

    def _create_drag_drop_area(self):
        """Create the drag and drop functionality for images.
        Created for new templates."""

        if not self._tierlist_id:
            self.dnd_area = ttk.Frame(self._root)
            self.dnd_area.place(x=400, y=700, anchor='n')

            self.drop_label = tk.Label(self.dnd_area, text='Drag image(s) here',
                                       width=20, height=3, bg='green')

            self.drop_label.grid(row=0, column=0)

            # Register the drop area for drag and drop
            self.dnd_area.drop_target_register(DND_FILES)
            self.dnd_area.dnd_bind('<<Drop>>', self._on_drop)

            self.drop_label.bind('<Enter>', self._on_hover)
            self.drop_label.bind('<Leave>', self._on_leave)

            self.dnd_area.dnd_bind('<<DropEnter>>', self._on_hover)
            self.dnd_area.dnd_bind('<<DropLeave>>', self._on_leave)

            self._canvas.create_text(260, 775, anchor='w', text='Most of the image formats supported',
                                     font=('Arial', 12, 'bold'))

    def _create_back_button(self):
        """Create back button to lists."""

        back = self._canvas.create_text(
            0, self._tier_count + 100, anchor='w', text="Back", font=('Arial', 20, 'bold'), fill='blue')

        self._canvas.tag_bind(
            back, '<Button-1>', lambda e: self._handle_show_list_view())

    def _create_create_button(self):
        """Create back button to lists."""

        if not self._tierlist_id:
            create = self._canvas.create_text(
                0, self._tier_count + 150, anchor='w', text="Create", font=('Arial', 20, 'bold'), fill='blue')

            self._canvas.tag_bind(
                create, '<Button-1>', lambda e: self._create_new_tier_list())

    def _on_drop(self, event):
        """Handle the event when an item is dropped."""

        # How to handle multiple images https://stackoverflow.com/a/77834313
        for i, path in enumerate(self._root.tk.splitlist(event.data)):

            if i == 5:
                print('For now max 5 items dropped at the same time supported')
                break

            # Position where the items will be placed
            x, y = (i + 1) * 120, self._tier_count

            # Add the image item
            image_item = self._item_service.add_item(path, x, y)

            # Place the image on the canvas
            item_id = self._canvas.create_image(x, y, image=image_item.image)
            self._canvas.image = image_item.image

            # Store the image_item
            self._item_map[item_id] = image_item

            # Bind drag movement event
            self._canvas.tag_bind(item_id, '<B1-Motion>', lambda e,
                                  id=item_id: self._on_drag(e, id))
            self._canvas.tag_bind(
                item_id, '<ButtonRelease-1>', self._on_drop_item)

    def _on_drag(self, event, item_id):
        """Move the item as the mouse moves."""
        x = self._canvas.canvasx(event.x)
        y = self._canvas.canvasy(event.y)

        self._canvas.coords(item_id, x, y)

    def _on_drop_item(self, event):
        """Snap the item to the closest tier."""
        x = self._canvas.canvasx(event.x)
        y = self._canvas.canvasy(event.y)

        # From https://stackoverflow.com/a/7604311
        item_id = self._canvas.find_withtag("current")[0]

        # Retrieve the image_item
        item = self._item_map.get(item_id)

        # Find the closest tier to the current Y position
        snapped_item = self._item_service.snap_item_to_tier(
            item, self.tier_positions, y)

        # Update the item position
        self._canvas.coords(item_id, x, snapped_item.y)

    def _create_new_tier_list(self):
        # Creates a list of image paths
        items = [item.image_path for key, item in self._item_map.items()]
        self._tier_list_service.create_tier_list_template(
            self._tier_list_name, self._tiers, items)

        # Return to list view
        self._handle_show_list_view()


"""These classes were originally in services and entities
but moved here because these only handle item moving in UI.
Will probably be replaced by more elegant system."""


class ItemHandler:
    def __init__(self):
        # For now used just for ids
        self._items = []

    def add_item(self, image_path, x, y):
        """Adds a new image item."""
        image = ImageRepository.load_image(image_path)
        item_id = f"item_{len(self._items)}"
        image_item = ImageItem(image, image_path, item_id, x, y)

        self._items.append(image_item)

        return image_item

    def snap_item_to_tier(self, item, tier_positions, event_y):
        """Snap the item to the closest tier."""

        # Idea for finding the shortest distance from
        # https://medium.com/@zzysjtu/python-min-function-a-deep-dive-f72cbd771872
        closest_tier = min(tier_positions, key=lambda y: abs(event_y - y))
        item.update_position(item.x, closest_tier)

        return item


class ImageItem:
    def __init__(self, image, image_path, item_id, x, y):
        self.image = image
        self.image_path = image_path
        self.item_id = item_id
        self.x = x
        self.y = y

    def update_position(self, x, y):
        self.x = x
        self.y = y
