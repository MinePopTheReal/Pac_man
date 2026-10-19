from numpy import frombuffer, uint8
from pyglet import image


class Layer:
    def __init__(self, width: int, height: int, format: str):
        self.width = width
        self.height = height
        self.format = format
        self.bytes_per_pixel = len(self.format)
        self.pitch = width * self.bytes_per_pixel

        self._create_layer()

    def _create_layer(self):
        self.buffer = bytearray(int(self.pitch * self.height))
        self.buffer_view = frombuffer(self.buffer, dtype=uint8).reshape(self.height, self.width, self.bytes_per_pixel)[::-1]

    def clear(self):
        self.buffer_view.fill(0)

    def draw(self, x: int, y: int):
        img = image.ImageData(
            self.width, self.height,
            self.format,
            bytes(self.buffer),
            pitch=self.pitch
        )
        img.blit(x, y)
