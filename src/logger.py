import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Logger:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
