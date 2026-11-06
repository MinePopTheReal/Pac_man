from src.utils.widget.widget import Widget, make_text_layer, Align
from src.utils.sprite_sheet_manager import SpriteSheetManager


class MenuItem:
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
        (self.selected if is_selected else self.normal).draw(x, y)


class Menu(Widget):
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
        self.selected = (self.selected + delta) % len(self.items)

    def _render(self) -> None:
        top = self.bottom + self.height
        for i, item in enumerate(self.items):
            item_x = self.left + (self.width - item.width) // 2
            item_y = top - self.zoom - i * (self.zoom + self.gap)
            item.draw(item_x, item_y, i == self.selected)
