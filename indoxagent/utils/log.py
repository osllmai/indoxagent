import logging
from rich.logging import RichHandler

logger = logging.getLogger("indoxagent")
handler = RichHandler(show_time=False)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
