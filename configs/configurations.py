from pathlib import Path
from configs.logger import get_logger


logger = get_logger("configurations")

GROQ_MODEL = "llama-3.1-8b-instant"
VISION_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
BASE_CACHE = ((Path.cwd()).resolve() / "cache").resolve()
BASE_DIR = (Path.cwd()).resolve()