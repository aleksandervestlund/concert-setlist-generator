import os
from pathlib import Path

import dotenv
from dacite import Config


dotenv.load_dotenv()
X_API_KEY = os.getenv("SETLIST_FM_API_KEY")

ROOT = Path(__file__).parent.parent.resolve()

TIMEOUT = 10.0
SLEEP_BETWEEN_REQUESTS = 1.0

VERSION = "1.0"
BASE_URL = f"https://api.setlist.fm/rest/{VERSION}"

CONFIG = Config(strict=True)
