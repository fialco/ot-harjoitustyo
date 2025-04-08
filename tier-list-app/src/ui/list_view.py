import tkinter as tk
from tkinter import ttk
from services.item_service import ItemService

class ListView:
    def __init__(self, root, handle_show_tier_list_view):
        self._root = root
        self._service = ItemService()

        self._handle_show_tier_list_view = handle_show_tier_list_view

        self.list = ['Programming Languages',
        'Linux Distros',
        'TV-series',
        'Albums',
        'Movies',
        'Games']

        self.frame = tk.Frame(self._root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for items and tiers
        self._canvas = tk.Canvas(self.frame, bg="snow2", height=800, width=800)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._draw_list()

    def pack(self):
        """"Show view."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """"Destory view."""
        self.frame.destroy()

    def on_button_click(self, name):
        #Button testing
        print(f"Chose tier list: {name}")
        self._handle_show_tier_list_view()

    def _draw_list(self):
        """Draw list of different tier lists."""

        for i in range(len(self.list)):
            y_position = i * 50
            self._canvas.create_rectangle(0, y_position-25, 800, y_position + 25,
                                         outline='black', width=2, fill='azure')

            self._canvas.create_text(5,  y_position, anchor='w', text=f"{self.list[i]}",
                                                font=('Arial', 25, 'bold'))

            button = self._canvas.create_text(750, y_position, text="Choose")
            self._canvas.tag_bind(button, '<Button-1>', lambda e, i=i: self.on_button_click(self.list[i]))

        scrollbar = ttk.Scrollbar(self.frame, command=self._canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Config canvast to use the scrollbar
        self._canvas.config(yscrollcommand=scrollbar.set)

        self._canvas.config(scrollregion=self._canvas.bbox("all"))

