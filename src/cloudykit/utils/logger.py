import loguru

logger = loguru.logger
logger.add("logs/cloudyapp_{time:YYYY-MM-DD}.log", rotation="5 MB")
