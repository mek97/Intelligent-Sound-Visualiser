import logging
import os
from pathlib import Path


class ConfigUtils:
    __OUTPUT_DIR = os.environ.get('INTELLIGENT_VISUALIZER_OUT', None)
    if not __OUTPUT_DIR:
        __OUTPUT_DIR = str(Path.home().joinpath("intelligent_visualizer"))
        logging.warning(f"Missing environment variable, defaulting to {__OUTPUT_DIR}")

    if not os.path.exists(__OUTPUT_DIR):
        logging.warning(f"Output directory does not exists, creating {__OUTPUT_DIR}")
        Path(__OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_output_directory(cls):
        return cls.__OUTPUT_DIR
