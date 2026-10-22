from numpy import frombuffer, uint8
from pyglet import image


class Layer:
    """
    allows you to create and manage a layer (so you can separate
    the maze rendering from the entities, for example)
    """
    def __init__(self, width: int, height: int, format: str):
        self.width = width
        self.height = height
        self.format = format
        self.bytes_per_pixel = len(self.format)
        self.pitch = width * self.bytes_per_pixel

        self._create_layer()

    def _create_layer(self) -> None:
        """
        Create the buffer and a buffer view that will allow transformations
        and calculations to be performed more
        quickly and efficiently using NumPy.
        """
        self.buffer = bytearray(int(self.pitch * self.height))
        self.buffer_view = frombuffer(self.buffer, dtype=uint8).reshape(
            self.height, self.width, self.bytes_per_pixel
        )[::-1]

    def clear(self) -> None:
        """
        Clears the buffer completely
        (for example, all pixels are set to R:0, G:0, B:0, A:0)
        """
        self.buffer_view.fill(0)

    def draw(self, x: int, y: int) -> None:
        """allows us to display our buffer in our Pyglet window

        Args:
            x (int): Coordinates (x) of the layer in the window
            y (int): Coordinates (y) of the layer in the window
        """
        img = image.ImageData(
            self.width,
            self.height,
            self.format,
            bytes(self.buffer),
            pitch=self.pitch,
        )
        img.blit(x, y)
