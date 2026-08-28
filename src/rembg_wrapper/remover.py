from enum import StrEnum
from pathlib import Path
from typing import cast

from PIL import Image
from PIL.Image import Image as PILImage
from rembg import new_session, remove


class ModelName(StrEnum):
    U2NET = "u2net"
    U2NETP = "u2netp"
    U2NET_HUMAN_SEG = "u2net_human_seg"
    U2NET_CLOTH_SEG = "u2net_cloth_seg"
    SILUETA = "silueta"
    ISNET_GENERAL_USE = "isnet-general-use"
    ISNET_ANIME = "isnet-anime"
    SAM = "sam"
    BIREFNET_GENERAL = "birefnet-general"
    BIREFNET_GENERAL_LITE = "birefnet-general-lite"
    BIREFNET_PORTRAIT = "birefnet-portrait"
    BIREFNET_DIS = "birefnet-dis"
    BIREFNET_HRSOD = "birefnet-hrsod"
    BIREFNET_COD = "birefnet-cod"
    BIREFNET_MASSIVE = "birefnet-massive"
    BRIA_RMBG = "bria-rmbg"


class Remover:
    def __init__(self, model_name: ModelName) -> None:
        self._model_name = model_name
        self._session = new_session(model_name.value)

    def remove(self, input_path: Path, output_path: Path) -> None:
        with Image.open(input_path) as input_image:
            output_image = cast(
                PILImage,
                remove(
                    input_image,
                    session=self._session,
                ),
            )

            output_image.save(output_path)
