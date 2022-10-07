import logging
import sys
from uvicorn import Config, Server
from src.core.init_application import application
from loguru import logger
from src.core.config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger_text = record.getMessage().split(" - ")
        if len(logger_text) > 1:
            if logger_text[1] != '"GET /healthcheck HTTP/1.1" 200':
                logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
        else:
            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())



def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.getLevelName("INFO"))

    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])


if __name__ == "__main__":
    try:
        server = Server(
            Config(app=application,
                   host=settings.http_server_host,
                   port=settings.http_server_port,
                   workers=settings.http_server_workers,
                   debug=settings.debug,
                   reload=settings.reload,
                   )

        )
        setup_logging()
        server.run()
    except Exception as e:
        print(e, flush=True)
        exit(1)
