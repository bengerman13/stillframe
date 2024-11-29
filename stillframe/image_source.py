import pathlib

from stillframe.config import Config


class FileWalkerImageSource:

    def __init__(self, source_path: pathlib.Path, extensions: list[str]):
        self.path = source_path
        self.extensions = extensions
        self.stills = []
        self.rescan()
        self.current_still_index = 0
        self.still_metadata = {}

    def rescan(self):
        stills = []
        for extension in self.extensions:
            stills.extend(self.path.glob(f"**/*.{extension}"))
        self.stills = sorted(stills)
        self.current_still_index = 0

    def get_next_still(self):
        with open(self.stills[self.current_still_index], "rb") as f:
            self.current_still_index += 1
            return f.read()
