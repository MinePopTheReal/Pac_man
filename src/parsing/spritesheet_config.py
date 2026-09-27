from src.utils.file_manager import FileManager
from json import loads
from dataclasses import dataclass
from pydantic import BaseModel, StrictInt, Field, ConfigDict, field_validator


class Coord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    x: StrictInt = Field(ge=0)
    y: StrictInt = Field(ge=0)


class Sprite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1)
    coord: list[Coord]


class Spritesheet(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tiles: list[Sprite]
    tile_size: int = Field(ge=1)

    @field_validator("tiles", mode="before")
    @classmethod
    def create_coord(
        cls, values: dict[str, list[dict[str, int]]]
    ) -> list[Sprite]:
        return [
            Sprite(name=key, coord=[Coord(**coord) for coord in value])
            for key, value in values.items()
        ]


class SpritesheetsConfigs(dataclass):
    maze_spritesheet: Spritesheet
    entities_spritesheet: Spritesheet


class SpritesheetConfigParser:
    def __init__(self) -> None:
        self.maze_config_file_path: str = "assets/maze_spritesheet_config.json"
        self.entities_config_file_path: str = (
            "assets/"
            "entities_spritesheet_config.json"
        )

    @staticmethod
    def load_config(path: str) -> Spritesheet:
        file_content = FileManager.read(path)
        file_datas = loads(file_content)

        spritesheet = Spritesheet(**file_datas)
        return spritesheet

    def save_config(self) -> SpritesheetsConfigs:
        maze_spritesheet = self.load_config(self.maze_config_file_path)
        entities_spritesheet = self.load_config(self.entities_config_file_path)
        return SpritesheetsConfigs(
            maze_spritesheet=maze_spritesheet,
            entities_spritesheet=entities_spritesheet
        )



condfig = SpritesheetConfigParser().save_config()
condfig.maze_spritesheet
