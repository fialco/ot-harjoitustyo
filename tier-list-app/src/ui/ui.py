from ui.tier_list_view import TierListView
from ui.list_view import ListView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_tier_list_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_tier_list_view(self):
        self._hide_current_view()

        self._current_view = TierListView(
            self._root,
            self._show_list_view
        )

        self._current_view.pack()

    def _show_list_view(self):
        self._hide_current_view()

        self._current_view = ListView(
            self._root,
            self._show_tier_list_view
        )

        self._current_view.pack()

