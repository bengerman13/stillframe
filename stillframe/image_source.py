import base64
import json
import pathlib

from dataclasses import dataclass, asdict

from stillframe.config import Config


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

    def to_json(self) -> str:
        d = asdict(self)
        d.pop("source")
        return json.dumps(d)

    def hydrate(self):
        with open(self.source, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            self.image_data = f"data:{self.mime_type};base64,{b64}"

    def dehydrate(self):
        self.image_data = ""


class FileWalkerImageSource:

    def __init__(self, source_path: pathlib.Path, extensions: list[str]):
        self.path = source_path
        self.extensions = extensions
        self.stills: list[Still] = []
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
                    id_=str(path),
                    mime_type=mime,
                    is_denylisted=False,
                    source=path,
                    image_data="",
                )
                if still.id_ not in self.stills_by_id:
                    stills.append(still)
                    self.stills_by_id[still.id_] = still
        self.stills.extend(stills)
        self.stills.sort(key=lambda x: x.source)
        self.current_still_index = 0

    def get_next_still(self) -> (Still, bytes):
        last_still = self.stills[self.current_still_index]
        self.current_still_index += 1
        while (next_still := self.stills[self.current_still_index]).is_denylisted:
            self.current_still_index += 1
        next_still.hydrate()
        last_still.dehydrate()
        return next_still
