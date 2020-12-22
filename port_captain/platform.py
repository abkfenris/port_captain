"""
IOOS Platform configuration loader and validation
"""
import pathlib
from typing import Dict, Optional, List

from pydantic import EmailStr
from pydantic_yaml import YamlEnum, YamlModel


class PlatformType(str, YamlEnum):
    buoy = "buoy"


class PlatformMaintainer(YamlModel):
    organization: str
    name: str
    email: EmailStr


class Platform(YamlModel):
    name: str
    region: str
    maintainer: PlatformMaintainer
    type: PlatformType


class ProcessingStep(YamlModel):
    slug: str
    meta: Dict


class Thing(YamlModel):
    platform: Platform
    processing: List[ProcessingStep]
    path: Optional[pathlib.Path]

    @classmethod
    def parse_yaml(cls, path: pathlib.Path):
        """ Parse a YAML definition into a Thing """
        thing = cls.parse_file(path, content_type="application/yaml")
        thing.path = path

        return thing
