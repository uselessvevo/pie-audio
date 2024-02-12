import sys
import loguru


logger = loguru.logger
logger.remove()
logger.add(
    sys.stderr,
    level="CRITICAL",
    format="<green>[{time:HH:mm:ss}] [{level}]</green>"
           "<white> - {name}:{function}:{line}</white> - <yellow>{message}</yellow>"
)

logger.add(
    "logs/pieaduio_{time:YYYY-MM-DD}.log",
    rotation="5 MB",
    format="[{time:HH:mm:ss}] [{level}] - {name}:{function}:{line} - {message}"
)
