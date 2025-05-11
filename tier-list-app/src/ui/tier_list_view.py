import tkinter as tk
import uuid
from tkinter import ttk, simpledialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

from services.tier_list_service import TierListService


class TierListView:
    """View, which handles new and already made tier list templates.
    """

    def __init__(self, root, handle_show_list_view, tierlist_id):
        """Class constructor. Creates the tier list view.

        Args:
            root:
                TKinterDND-element, into which the user interface is initialized.
            handle_show_list_view:
                Is called when we want go get back to list view.
            tierlist_id:
                Has value None if 'New template' picked, otherwise it's the id of the tier list being chosen.
        """

        self._root = root

        self.service = TierListService()

        self._handle_show_list_view = handle_show_list_view

        self._tierlist_id = tierlist_id

        self._frame = tk.Frame(self._root)
        self._frame.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(
            self._frame, bg="snow2", height=900, width=800)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tier_height = 100

        self._item_map = {}
        self._tier_map = {}

        self._init_tier_list_data()

        self._draw_tiers()

        self._create_drag_drop_area()

        if self._tierlist_id is not None:
            self._draw_items()

        self._create_back_button()
        self._create_create_button()
        self._create_screenshot_button()
        self._create_text_to_image_button()

        scrollbar = ttk.Scrollbar(self._frame, command=self._canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._canvas.config(yscrollcommand=scrollbar.set)
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def pack(self):
        """Show view."""
        self._frame.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """Destory view."""
        self._frame.destroy()

    def _ask_tier_count(self):
        min_count = 2
        max_count = 10

        while True:
            count = simpledialog.askinteger(
                title='Tier count', prompt=f'How many tiers from {min_count} to {max_count}?', parent=self._frame)

            if count is None:
                continue

            elif min_count <= count <= max_count:
                return count

            messagebox.showerror(
                'Invalid Input', 'Please enter a valid integer.')

    def _init_tier_list_data(self):
        self._tier_list_name = 'Click here to name the tier list'

        if not self._tierlist_id:
            count = self._ask_tier_count()
            names = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
            self._tiers = dict(zip(range(count), names))

        if self._tierlist_id:
            tier_list = self.service.get_tier_list(
                self._tierlist_id)
            self._tier_list_name = tier_list.name

            tier_data = self.service.get_tiers_of_tier_list(
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
            self.canvas_tier_list_name, '<Button-1>', lambda e: self._change_tier_list_name())

        for rank, tier in self._tiers.items():
            self._canvas.create_rectangle(0, self.tier_positions[rank] - self.tier_height // 2,
                                          800, self.tier_positions[rank] +
                                          self.tier_height // 2,
                                          outline='black', width=2, fill='azure')

            tier_id = self._canvas.create_text(10, self.tier_positions[rank], anchor='w', text=f"{tier}",
                                               font=('Arial', 16, 'bold'), width=100)

            self._tier_map[tier_id] = rank

            if not self._tierlist_id:
                self._canvas.tag_bind(
                    tier_id, '<Button-1>', lambda e, tier=tier: self._change_tier_name(tier))

        self._canvas.create_rectangle(0, self._tier_count - self.tier_height // 2,
                                      800, self._tier_count +
                                      self.tier_height // 2,
                                      outline='black', width=2, fill='gray80')

    def _draw_items(self):
        items = self.service.get_items_of_tier_list(
            self._tierlist_id)

        base_dir = self.service.get_base_dir_path()

        for i, item in enumerate(items):
            x, y = (i + 1) * 120, self._tier_count

            image_path = base_dir + item.image_path

            image_item = ItemHandler(self.service, x, y, image_path=image_path)

            item_id = self._canvas.create_image(
                x, y, image=image_item.photo_image)
            self._canvas.image = image_item.photo_image

            self._item_map[item_id] = image_item

            self._canvas.tag_bind(item_id, '<B1-Motion>', lambda e,
                                  id=item_id: self._on_drag(e, id))
            self._canvas.tag_bind(
                item_id, '<ButtonRelease-1>', self._on_drop_item)

    def _on_hover(self, event):
        self.drop_label.config(bg='yellow')

    def _on_leave(self, event):
        self.drop_label.config(bg='green')

    def _create_drag_drop_area(self):
        """Create the drag and drop functionality for images."""

        if not self._tierlist_id:
            self.dnd_area = ttk.Frame(self._canvas)

            self._canvas.create_window(
                400, self._tier_count+100, anchor="n", window=self.dnd_area)

            self.drop_label = tk.Label(self.dnd_area, text='Drag image(s) here',
                                       width=20, height=3, bg='green')

            self.drop_label.grid(row=0, column=0)

            self.dnd_area.drop_target_register(DND_FILES)
            self.dnd_area.dnd_bind('<<Drop>>', self._on_drop)

            self.drop_label.bind('<Enter>', self._on_hover)
            self.drop_label.bind('<Leave>', self._on_leave)

            self.dnd_area.dnd_bind('<<DropEnter>>', self._on_hover)
            self.dnd_area.dnd_bind('<<DropLeave>>', self._on_leave)

    def _create_back_button(self):
        back = self._canvas.create_text(
            0, self._tier_count + 100, anchor='w', text="Back", font=('Arial', 20, 'bold'), fill='blue')

        self._canvas.tag_bind(
            back, '<Button-1>', lambda e: self._handle_show_list_view())

    def _create_create_button(self):
        if not self._tierlist_id:
            create = self._canvas.create_text(
                0, self._tier_count + 150, anchor='w', text="Create", font=('Arial', 20, 'bold'), fill='blue')

            self._canvas.tag_bind(
                create, '<Button-1>', lambda e: self._create_new_tier_list())

    def _create_text_to_image_button(self):
        if not self._tierlist_id:
            create = self._canvas.create_text(
                500, self._tier_count+130, anchor='w', text="Add text image", font=('Arial', 20, 'bold'), fill='blue')

            self._canvas.tag_bind(
                create, '<Button-1>', lambda e: self._handle_text_to_image())

    def _create_screenshot_button(self):
        if self._tierlist_id:
            screenshot = self._canvas.create_text(
                0, self._tier_count + 150, anchor='w', text="Screenshot", font=('Arial', 20, 'bold'), fill='blue')

            self._canvas.tag_bind(
                screenshot, '<Button-1>', lambda e: self._handle_screenshot())

    def _on_drop(self, event):
        """Handle the event when an item is dropped.
        How to handle multiple images https://stackoverflow.com/a/77834313."""

        for i, path in enumerate(self._root.tk.splitlist(event.data)):

            if i == 5:
                print('For now max 5 items dropped at the same time supported')
                break

            x, y = (i + 1) * 120, self._tier_count

            image_item = ItemHandler(self.service, x, y, image_path=path)

            if image_item.photo_image is None:
                break

            item_id = self._canvas.create_image(
                x, y, image=image_item.photo_image)
            self._canvas.image = image_item.photo_image

            self._item_map[item_id] = image_item

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

        item_id = self._canvas.find_withtag("current")[0]

        item = self._item_map.get(item_id)

        snapped_item = item.snap_item_to_tier(
            item, self.tier_positions, x, y)

        self._canvas.coords(item_id, snapped_item.x, snapped_item.y)

    def _create_new_tier_list(self):
        image_paths = [item.image_path for key, item in self._item_map.items()]
        self.service.create_tier_list_template(
            self._tier_list_name, self._tiers, image_paths)

        self._handle_show_list_view()

    def _handle_screenshot(self):
        image_name = self.service.take_canvas_screenshot(self._canvas)
        messagebox.showinfo(
            'Screenshot', f'Image {image_name} saved to data/screenshots/')

    def _handle_text_to_image(self):
        while True:
            text = simpledialog.askstring(
                title='Text to image', prompt='Input text (max 55 characters):', parent=self._root)

            if text is None:
                break

            if 1 <= len(text) <= 55:
                x, y = 700, 700

                image_item = ItemHandler(self.service, x, y, text=text)

                item_id = self._canvas.create_image(
                    x, y, image=image_item.photo_image)
                self._canvas.image = image_item.photo_image

                self._item_map[item_id] = image_item

                self._canvas.tag_bind(item_id, '<B1-Motion>', lambda e,
                                      id=item_id: self._on_drag(e, id))
                self._canvas.tag_bind(
                    item_id, '<ButtonRelease-1>', self._on_drop_item)

                break

            messagebox.showerror('Invalid Input', 'Please enter a valid text.')

    def _handle_name_input(self, max_len):
        while True:
            name = simpledialog.askstring(
                title='Tier name', prompt=f'Input a name (max {max_len} characters):', parent=self._root)

            if name is None:
                break

            if 1 <= len(name) <= max_len:
                return name

            messagebox.showerror('Invalid Input', 'Please enter a valid name.')

    def _change_tier_list_name(self):
        if not self._tierlist_id:
            name = self._handle_name_input(28)

            if name:
                self._canvas.itemconfig(self.canvas_tier_list_name, text=name)
                self._tier_list_name = name

    def _change_tier_name(self, tier_id):
        if not self._tierlist_id:
            tier_id = self._canvas.find_withtag("current")[0]
            tier = self._tier_map.get(tier_id)

            name = self._handle_name_input(20)

            if name:
                self._tiers[tier] = name
                self._canvas.itemconfig(tier_id, text=name)


class ItemHandler:
    """Class, which handles items on tier list."""

    def __init__(self, service, x, y, image_path=None, text=None):
        """Class constructor. Creates a new item.

        Args:
            service:
                TierListService-object used for loading an image.
            x:
                x coordinate of the item on a window
            y:
                t coordinate of the item on a window
            image_path:
                Optional, Absolute path of the image.
            text:
                Optional, Value to be made an image.

        """

        if image_path:
            self.photo_image = self.get_image(service, image_path)
            self.image_path = image_path
        elif text:
            self.photo_image, self.image_path = service.text_to_image(text)

        self.item_id = uuid.uuid4().int
        self.x = x
        self.y = y
        self.text = text

    def get_image(self, service, image_path):
        """Handles image loading.

        Args:
            service:
                TierListService-object used for loading an image.
            image_path:
                Absolute path of the image.

        Returns:
            image-item
        """

        try:
            return service.get_image(image_path)

        except ValueError as ve:
            messagebox.showerror("Format Error", str(ve))

        except FileNotFoundError as ve:
            messagebox.showerror("File Error", str(ve))

    def update_position(self, x, y):
        """Updates items coordinates.

        Args:
            x:
                x coordinate of the item on a window
            y:
                t coordinate of the item on a window
        """

        self.x = x
        self.y = y

    def snap_item_to_tier(self, item, tier_positions, event_x, event_y):
        """Snap the item to the closest tier.
        Finding the shortest distance
        https://medium.com/@zzysjtu/python-min-function-a-deep-dive-f72cbd771872

        Args:
            item:
                Item to be snapped to tier.
            tier_positions:
                Coordinates where the item should be snapped.
            event_x:
                Current x coordinate of the item.
            event_y:
                Current y coordinate of the item.

        Returns:
            Item with updated coordinates
        """
        closest_tier = min(tier_positions, key=lambda y: abs(event_y - y))

        event_x = max(50, min(event_x, 750))

        item.update_position(event_x, closest_tier)

        return item
