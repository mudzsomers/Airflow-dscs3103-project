
import pandas as pd
from src.common.config import SOURCE_A_RAW_PATH


def ingest_source_a(path: str=SOURCE_A_RAW_PATH)-> pd.DataFrame:
    df = pd.read_csv(path)
    return df 