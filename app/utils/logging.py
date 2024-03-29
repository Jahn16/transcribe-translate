import logging
import sys

import structlog


def setup_logging() -> None:
    disable_uvicorn_logs()
    configure_structlog()


def disable_uvicorn_logs() -> None:
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.disabled = True
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.disabled = True


def configure_structlog() -> None:
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        structlog.processors.StackInfoRenderer(),
    ]
    if sys.stderr.isatty():
        # DEV MODE
        log_level = logging.DEBUG
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # PROD MODE
        log_level = logging.INFO
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
    structlog.configure(
        processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )
