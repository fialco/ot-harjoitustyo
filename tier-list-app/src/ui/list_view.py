import tkinter as tk
from tkinter import ttk, messagebox

from services.tier_list_service import TierListService


class ListView:
    def __init__(self, root, handle_show_tier_list_view):
        self._root = root
        self._service = TierListService()

        self._handle_show_tier_list_view = handle_show_tier_list_view

        self.frame = tk.Frame(self._root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for items and tiers
        self._canvas = tk.Canvas(self.frame, bg="snow2", height=900, width=800)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._initialize()

    def pack(self):
        """Show view."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """Destory view."""
        self.frame.destroy()

    def _choose_button_click(self, tier_list):
        self._handle_show_tier_list_view(tier_list.id)

    def _delete_button_click(self, tier_list):
        if messagebox.askyesno(title='Delete tier list?',
                               message=f'Are you sure you want to delete tier list {tier_list.name}?'):

            self._service.delete_tier_list(tier_list.id)
            self._draw_items()

    def _new_button_click(self):
        self._handle_show_tier_list_view()

    def _initialize(self):
        scrollbar = ttk.Scrollbar(self.frame, command=self._canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Config canvast to use the scrollbar
        self._canvas.config(yscrollcommand=scrollbar.set)

        self._canvas.config(scrollregion=self._canvas.bbox("all"))

        self._draw_items()

    def _draw_items(self):
        self._canvas.delete('all')
        self._list = self._service.get_tier_lists()

        # New template box and button
        self._canvas.create_rectangle(0, 0, 800, 75,
                                      outline='black', width=2, fill='SpringGreen2')

        new = self._canvas.create_text(
            400, 30, text="New template", font=('Arial', 25, 'bold'), fill='blue')

        self._canvas.tag_bind(
            new, '<Button-1>', lambda e: self._new_button_click())

        for i in range(len(self._list)):
            y_position = (i+2) * 50
            self._canvas.create_rectangle(0, y_position-25, 800, y_position + 25,
                                          outline='black', width=2, fill='azure')

            self._canvas.create_text(5,  y_position, anchor='w', text=f"{self._list[i].name}",
                                     font=('Arial', 18, 'bold'))

            choose = self._canvas.create_text(
                730, y_position, text="Choose", font=('Arial', 15, 'bold'), fill='blue')

            self._canvas.tag_bind(
                choose, '<Button-1>', lambda e, i=i: self._choose_button_click(self._list[i]))

            delete = self._canvas.create_text(
                785, y_position, text="X", font=('Arial', 20, 'bold'), fill='red')

            self._canvas.tag_bind(
                delete, '<Button-1>', lambda e, i=i: self._delete_button_click(self._list[i]))
