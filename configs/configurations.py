from pathlib import Path

from configs.logger import get_logger

logger = get_logger("configurations")

GROQ_MODEL = "llama-3.1-8b-instant"
VISION_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
BASE_CACHE = ((Path.cwd()).resolve() / "cache").resolve()
BASE_DIR = (Path.cwd()).resolve()
STORAGE_DIR =  (Path.cwd() / "storage" / "resumes").resolve()
JOB_RELEVANCY_THRESHOLD = 80

TOPJOB_MCP_SERVER_HOST = "127.0.0.1"
TOPJOB_MCP_SERVER_PORT = 9000
TOPJOB_SERVER_URL = f"http://{TOPJOB_MCP_SERVER_HOST}:{TOPJOB_MCP_SERVER_PORT}"