import base64
import hashlib
from collections import deque
from dataclasses import dataclass, asdict
import json
import pathlib

from stillframe.popdeque import Popdeque


def mime_for_extension(extension: str) -> str:
    if extension == "jpg":
        extension = "jpeg"
    return f"image/{extension}"


@dataclass
class Still:
    id_: str
    mime_type: str
    is_denylisted: bool
    source: str
    image_data: str
    is_hydrated: bool = False

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d)

    def hydrate(self):
        with open(self.source, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            self.image_data = f"data:{self.mime_type};base64,{b64}"
            self.is_hydrated = True

    def dehydrate(self):
        self.image_data = ""
        self.is_hydrated = False


class FileWalkerImageSource:

    def __init__(self, source_path: pathlib.Path, extensions: list[str]):
        self.path = source_path
        self.extensions = extensions
        self.stills: deque[Still] = deque()
        self.recent_stills: Popdeque[Still] = Popdeque(maxlen=10)
        self.stills_by_id = {}
        self.rescan()
        self.current_still_index = 0

    def rescan(self):
        stills = []
        for extension in self.extensions:
            mime = mime_for_extension(extension)
            for path in self.path.glob(f"**/*.{extension}"):
                still = Still(
                    # TODO: use something other than path as id
                    id_=hashlib.md5(str(path).encode("utf-8")).hexdigest(),
                    mime_type=mime,
                    is_denylisted=False,
                    source=str(path),
                    image_data="",
                )
                if still.id_ not in self.stills_by_id:
                    stills.append(still)
                    self.stills_by_id[still.id_] = still
        stills.sort(key=lambda x: x.source)
        self.stills.clear()
        self.stills.extend(stills)

    def get_next_still(self) -> (Still, bytes):
        self.stills.rotate(-1)
        while self.stills[0].is_denylisted:
            self.stills.rotate(-1)
        dropped = self.recent_stills.append(self.stills[-1])
        if dropped is not None:
            dropped.dehydrate()
        self.stills[0].hydrate()
        return self.stills[0]
