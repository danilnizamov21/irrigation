import logging


def configure_logging():
    formatter = logging.Formatter(
        "%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.basicConfig(level=logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    error_handler = logging.FileHandler("error.log", mode="a", encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logging.getLogger().addHandler(error_handler)
