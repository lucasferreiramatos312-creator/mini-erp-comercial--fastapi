import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="sistema.log",
    encoding="utf-8" 
)

logger = logging.getLogger("erp")