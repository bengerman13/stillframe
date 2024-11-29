from stillframe.config import Config
from stillframe.image_source import FileWalkerImageSource

CONFIG = Config.from_env()
IMAGE_SOURCE = FileWalkerImageSource(CONFIG.source_path, CONFIG.extensions)
