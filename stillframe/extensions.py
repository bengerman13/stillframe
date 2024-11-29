from stillframe.config import Config
from stillframe.image_source import FileWalkerImageSource
from stillframe.connection_manager import ConnectionManager

CONFIG = Config.from_env()
IMAGE_SOURCE = FileWalkerImageSource(CONFIG.source_path, CONFIG.extensions)
CONNECTION_MANAGER = ConnectionManager()
