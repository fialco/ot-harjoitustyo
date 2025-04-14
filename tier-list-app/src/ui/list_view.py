import tkinter as tk
from tkinter import ttk

from services.tier_list_service import TierListService


class ListView:
    def __init__(self, root, handle_show_tier_list_view):
        self._root = root
        self._service = TierListService()

        self._handle_show_tier_list_view = handle_show_tier_list_view

        self.list = self._service.get_tier_lists()

        self.frame = tk.Frame(self._root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for items and tiers
        self._canvas = tk.Canvas(self.frame, bg="snow2", height=900, width=800)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._draw_list()

    def pack(self):
        """Show view."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """Destory view."""
        self.frame.destroy()

    def choose_button_click(self, tier_list):
        self._handle_show_tier_list_view(tier_list.id)

    def new_button_click(self):
        self._handle_show_tier_list_view()

    def _draw_list(self):
        """Draw list of different tier lists."""

        if len(self.list) == 0:
            self._canvas.create_text(0, 0,  anchor='n', text="List empty, please run 'poetry run invoke build'.",
                                     font=('Arial', 25, 'bold'))

        # New template box and button
        self._canvas.create_rectangle(0, 0, 800, 75,
                                      outline='black', width=2, fill='SpringGreen2')

        new = self._canvas.create_text(
            400, 30, text="New template", font=('Arial', 25, 'bold'), fill='blue')

        self._canvas.tag_bind(
            new, '<Button-1>', lambda e: self.new_button_click())

        for i in range(len(self.list)):
            y_position = (i+2) * 50
            self._canvas.create_rectangle(0, y_position-25, 800, y_position + 25,
                                          outline='black', width=2, fill='azure')

            self._canvas.create_text(5,  y_position, anchor='w', text=f"{self.list[i].name}",
                                     font=('Arial', 25, 'bold'))

            choose = self._canvas.create_text(
                750, y_position, text="Choose", font=('Arial', 15, 'bold'), fill='blue')

            self._canvas.tag_bind(
                choose, '<Button-1>', lambda e, i=i: self.choose_button_click(self.list[i]))

        scrollbar = ttk.Scrollbar(self.frame, command=self._canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Config canvast to use the scrollbar
        self._canvas.config(yscrollcommand=scrollbar.set)

        self._canvas.config(scrollregion=self._canvas.bbox("all"))
