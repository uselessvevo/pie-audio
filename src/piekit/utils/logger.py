import loguru

logger = loguru.logger
logger.add("../../logs/pieaduio_{time:YYYY-MM-DD}.log", rotation="5 MB")
