import logging
from pathlib import Path
from datetime import datetime


# ------------------------------------------------
# 로그 폴더 생성
# ------------------------------------------------

LOG_DIR = Path("../logs")
LOG_DIR.mkdir(exist_ok=True)

# ------------------------------------------------
# 로그 파일명
# ------------------------------------------------

LOG_FILE = LOG_DIR / (
    datetime.now().strftime("%Y%m%d") + ".log"
)

# ------------------------------------------------
# Logger 생성
# ------------------------------------------------

logger = logging.getLogger("travel_agent")

# 중복 Handler 방지
if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s\n%(message)s\n",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)