from pydantic import (BaseModel, StrictInt, Field, ConfigDict, field_validator,
                      ValidationError, ValidationInfo,
                      ValidatorFunctionWrapHandler, model_validator)
from typing import Any
from src.message.warning import WarningMessage


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


class GameConfig(BaseModel):
    highscore_filename: str = Field(default="highscores.json")
    lives: StrictInt = Field(default=3, ge=1)
    pacgum: StrictInt = Field(default=42, ge=0)
    points_pacgum: StrictInt = Field(default=10, ge=0)
    points_super_pacgum: StrictInt = Field(default=50, ge=0)
    points_ghost: StrictInt = Field(default=200, ge=0)
    seed: StrictInt = Field(default=42, ge=0)
    level_max_time: StrictInt = Field(default=90, ge=1)
    width: StrictInt = Field(default=22, ge=14, le=50)
    height: StrictInt = Field(default=22, ge=10, le=50)
    nb_level: StrictInt = Field(default=10, ge=10)

    @field_validator("*", mode="wrap")
    @classmethod
    def use_default_if_invalid(cls, value: Any,
                               handler: ValidatorFunctionWrapHandler,
                               info: ValidationInfo) -> Any:
        try:
            return handler(value)
        except ValidationError:
            if info.field_name is None:
                raise
            default = cls.model_fields[info.field_name].default
            print(WarningMessage(f"Invalid value for '{info.field_name}' "
                                 f"({value!r}), using default "
                                 f"{default} instead."))
            return default

    @model_validator(mode="after")
    def report_missing_key(self) -> 'GameConfig':
        for name, field in type(self).model_fields.items():
            if name not in self.model_fields_set:
                print(WarningMessage(f"key '{name}' is missing, "
                                     f"using default value {field.default}"))
        return self
