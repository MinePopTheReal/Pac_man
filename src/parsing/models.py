from pydantic import BaseModel, StrictInt, Field, ConfigDict, field_validator


class Coord(BaseModel):
    """
    Check if coord are valid
    """
    model_config = ConfigDict(extra="forbid")
    x: StrictInt = Field(ge=0)
    y: StrictInt = Field(ge=0)


class Spritesheet(BaseModel):
    """
    Check spritesheet config
    """
    model_config = ConfigDict(extra="forbid")
    tiles: dict[str, list[Coord]]
    tile_size: int = Field(ge=1)

    @field_validator("tiles", mode="before")
    @classmethod
    def create_coord(
        cls, values: dict[str, list[dict[str, int]]]
    ) -> dict[str, list[Coord]]:
        return {
            key: [Coord(**coord) for coord in value]
            for key, value in values.items()
            }
