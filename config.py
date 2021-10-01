import logging
import sys
from functools import partial
from pathlib import Path
from typing import Type, TypeVar

import attr
import cattr
import yaml

T = TypeVar("T")

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)


@attr.dataclass(frozen=True)
class App:
    string: str
    integer: int


@attr.dataclass(frozen=True)
class Dataset:
    string: str
    integer: int


def maybe_cast_from_yaml(attrib: Path, *, to_type: Type[T]) -> T:
    return (
        attrib
        if isinstance(attrib, to_type)
        else cattr.structure(yaml.safe_load(attrib.read_bytes()), to_type)
    )


@attr.dataclass(frozen=True)
class Config:
    app: App = attr.ib(
        converter=partial(
            maybe_cast_from_yaml,
            to_type=App,
        )
    )
    dataset: Dataset = attr.ib(
        converter=partial(
            maybe_cast_from_yaml,
            to_type=Dataset,
        )
    )
    debug: bool = attr.ib(default=False)
    secret_number: int = attr.ib(default=0)


c = Config(
    app=Path("./example.yaml"),
    dataset=Path("./example.yaml"),
)
