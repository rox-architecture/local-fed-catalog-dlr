import logging

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("local_fc")
logger.setLevel("DEBUG")
logger.addHandler(handler)
logger.propagate = False
