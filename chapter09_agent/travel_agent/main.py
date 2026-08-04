import warnings
import sys

from pathlib import Path
from dotenv import load_dotenv

from langchain_core._api.deprecation import (
    LangChainPendingDeprecationWarning
)

warnings.filterwarnings(
    "ignore",
    category=LangChainPendingDeprecationWarning
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chapter09_agent.travel_agent.ui.main_view import show_main


load_dotenv()


if __name__ == "__main__":
    show_main()