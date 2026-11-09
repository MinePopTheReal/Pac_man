from src.utils.widget.widget import Widget, make_text_layer, Align
from src.utils.sprite_sheet_manager import SpriteSheetManager


class MenuItem:
    """One entry of a menu, drawn in two colors.

    The text is drawn twice when the item is created: once in the normal
    color and once in the selected color. Showing the item as selected or
    not then only means choosing which of the two images to draw.
    """
    def __init__(
        self,
        text: str,
        zoom: int,
        font: SpriteSheetManager,
        normal_color: tuple[int, int, int],
        selected_color: tuple[int, int, int],
        align: Align = "center",
    ) -> None:
        self.normal = make_text_layer(text, zoom, font, normal_color, align)
        self.selected = make_text_layer(
            text, zoom, font, selected_color, align
        )
        self.width = self.normal.width

    def draw(self, x: int, y: int, is_selected: bool) -> None:
        """Draw the item in the window.

        Args:
            x (int): Horizontal position of the left of the item.
            y (int): Vertical position of the bottom of the item.
            is_selected (bool): True to draw it in the selected color,
                False for the normal color.
        """
        (self.selected if is_selected else self.normal).draw(x, y)


class Menu(Widget):
    """Widget that shows a vertical list of entries, one of them selected.

    The entries are stacked from top to bottom, centered horizontally,
    with a gap of one character between them. The selected entry is
    drawn in another color. The widget only displays the menu and keeps
    the position of the selection: the key presses are handled by the
    screen, which calls move().
    """
    def __init__(
        self,
        texts: list[str],
        zoom: int,
        font: SpriteSheetManager,
        normal_color: tuple[int, int, int],
        selected_color: tuple[int, int, int],
        *,
        x: int,
        y: int,
        anchor_x: float = 0.5,
        anchor_y: float = 0.5,
        blink_period: float | None = None,
    ) -> None:
        self.items = [
            MenuItem(t, zoom, font, normal_color, selected_color)
            for t in texts
        ]
        self.zoom = zoom
        self.gap = zoom
        self.selected = 0
        n = len(self.items)
        super().__init__(
            max(item.width for item in self.items),
            n * zoom + (n - 1) * self.gap,
            x=x,
            y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            blink_period=blink_period,
        )

    def move(self, delta: int) -> None:
        """Move the selection up or down.

        After the last entry the selection goes back to the first one,
        and the other way round.

        Args:
            delta (int): The number of entries to move: -1 selects the
                previous entry (up), 1 selects the next one (down).
        """
        self.selected = (self.selected + delta) % len(self.items)

    def _render(self) -> None:
        """Draw the entries one under the other, each one centered."""
        top = self.bottom + self.height
        for i, item in enumerate(self.items):
            item_x = self.left + (self.width - item.width) // 2
            item_y = top - self.zoom - i * (self.zoom + self.gap)
            item.draw(item_x, item_y, i == self.selected)
