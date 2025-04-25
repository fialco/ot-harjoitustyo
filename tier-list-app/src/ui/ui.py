from ui.tier_list_view import TierListView
from ui.list_view import ListView


class UI:
    """Class, which handles application's user interface."""

    def __init__(self, root):
        """Class constructor. Creates a class for user interface handling.

        Args:
            root:
                TKinterDND-element, into which the user interface is initialized.
        """

        self._root = root
        self._current_view = None

    def start(self):
        """Starts the user interface."""
        self._show_list_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_tier_list_view(self, tierlist_id=None):
        self._hide_current_view()

        self._current_view = TierListView(
            self._root,
            self._show_list_view,
            tierlist_id
        )

        self._current_view.pack()

    def _show_list_view(self):
        self._hide_current_view()

        self._current_view = ListView(
            self._root,
            self._show_tier_list_view,
        )

        self._current_view.pack()
