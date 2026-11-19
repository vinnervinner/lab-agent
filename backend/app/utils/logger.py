import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

agent_logger = logging.getLogger("agent")
if not agent_logger.handlers:
    agent_logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        LOG_DIR / "agent.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    agent_logger.addHandler(handler)
    agent_logger.propagate = False


def log_agent_event(event: str, **fields: object) -> None:
    """Write a compact, structured Agent event without logging user content."""
    payload = {"event": event, **fields}
    try:
        agent_logger.info(json.dumps(payload, ensure_ascii=False, default=str))
    except Exception:
        # Logging must never break the user's request.
        agent_logger.exception("failed_to_write_agent_log")
