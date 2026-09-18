from pathlib import Path
from configs.logger import get_logger


logger = get_logger("configurations")

GROQ_MODEL = "llama-3.1-8b-instant"
BASE_CACHE = ((Path.cwd()).resolve() / "cache").resolve()