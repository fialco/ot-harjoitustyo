import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from services.item_service import ItemService


class TierListView:
    def __init__(self, root, handle_show_list_view):
        self._root = root
        self._service = ItemService()

        self._handle_show_list_view = handle_show_list_view

        # Canvas for items and tiers
        self.canvas = tk.Canvas(root, bg="snow2", height=800, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._create_back_button()

        # Tiers defined by labels
        # Hard coded for now
        self.tiers = ['S', 'A', 'B', 'C', 'D']
        self.tier_positions = [100, 200, 300, 400, 500]
        self.tier_height = 100

        # Draw tiers on the canvas
        self._draw_tiers()

        # Dictionary to store item ID to ImageItem mapping
        # Proper storage later
        self._item_map = {}

        self._create_drag_drop_area()

    def pack(self):
        """Show view."""
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """Destory view."""
        self.canvas.destroy()

    def _draw_tiers(self):
        """Draw the tiers on the canvas."""

        # Adds the amount of tiers given
        for i, tier in enumerate(self.tiers):
            self.canvas.create_rectangle(0, self.tier_positions[i] - self.tier_height // 2,
                                         800, self.tier_positions[i] +
                                         self.tier_height // 2,
                                         outline='black', width=2, fill='azure')

            self.canvas.create_text(10, self.tier_positions[i], anchor='w', text=f"[{tier}]",
                                    font=('Arial', 35, 'bold'))

    # Change dropzone color with mouse hover
    def _on_hover(self, event):
        self.drop_label.config(bg='yellow')

    def _on_leave(self, event):
        self.drop_label.config(bg='green')

    def _on_drag_hover(self, event):
        self.drop_label.config(bg='yellow')

    def _on_drag_leave(self, event):
        self.drop_label.config(bg='green')

    def _create_drag_drop_area(self):
        """Create the drag and drop functionality for images."""
        self.dnd_area = ttk.Frame(self._root)
        self.dnd_area.place(x=400, y=700, anchor='n')

        self.drop_label = tk.Label(self.dnd_area, text='Drag image here',
                                   width=20, height=3, bg='green')

        self.drop_label.grid(row=0, column=0)

        # Register the drop area for drag and drop
        self.dnd_area.drop_target_register(DND_FILES)
        self.dnd_area.dnd_bind('<<Drop>>', self._on_drop)

        self.drop_label.bind('<Enter>', self._on_hover)
        self.drop_label.bind('<Leave>', self._on_leave)

        self.dnd_area.dnd_bind('<<DropEnter>>', self._on_drag_hover)
        self.dnd_area.dnd_bind('<<DropLeave>>', self._on_drag_leave)

        self.canvas.create_text(260, 775, anchor='w', text='Most of the image formats supported',
                                font=('Arial', 12, 'bold'))

    def _create_back_button(self):
        """Create back button to lists."""

        logout_button = ttk.Button(
            master=self.canvas,
            text="Back",
            command=self._handle_show_list_view
        )
        logout_button.place(x=0, y=0)

    def _on_drop(self, event):
        """Handle the event when an item is dropped."""
        image_path = event.data

        # Position where the item will be placed
        x, y = 400, 650

        # Add the image item
        image_item = self._service.add_item(image_path, x, y)

        # Place the image on the canvas
        item_id = self.canvas.create_image(x, y, image=image_item.image)
        self.canvas.image = image_item.image

        # Store the image_item
        self._item_map[item_id] = image_item

        # Bind drag movement event
        self.canvas.tag_bind(item_id, '<B1-Motion>', lambda e,
                             id=item_id: self._on_drag(e, id))
        self.canvas.tag_bind(item_id, '<ButtonRelease-1>', self._on_drop_item)

    def _on_drag(self, event, item_id):
        """Move the item as the mouse moves."""
        self.canvas.coords(item_id, event.x, event.y)

    def _on_drop_item(self, event):
        """Snap the item to the closest tier."""
        # From https://stackoverflow.com/a/7604311
        item_id = self.canvas.find_withtag("current")[0]

        # Retrieve the image_item
        item = self._item_map.get(item_id)

        # Find the closest tier to the current Y position
        snapped_item = self._service.snap_item_to_tier(
            item, self.tier_positions, event.y)

        # Update the item position
        self.canvas.coords(item_id, event.x, snapped_item.y)
