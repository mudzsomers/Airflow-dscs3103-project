import logging
from src.common.logging_setup import get_logger
from src.ingest.source_a import ingest_source_a

from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data
from src.validate.rules import rule_negative_rain
from src.common.config import merged_data_path


#logging.basicConfig(
  #  level=logging.INFO,
   # format="%(asctime)s | %(levelname)s | %(message)s"
#)
PATH= "data/processed/merged_prices_with_rain.parquet"
logger = get_logger()


def run_pipe():
    logger.info("=== Pipeline run started ===")


    logger.info("STAGE 1: Ingesting Source A - prices")
    source_a = ingest_source_a()
    logger.info(f"Stage 11 : Source a Ingested:   rows out:{len(source_a)}")
    #logger.info("Source A loaded: %d rows", len(source_a))
    logger.info("=" * 50)

    logger.info("STAGE 2: Ingesting Source B - rainfall")
    source_b = ingest_source_b()
    logger.info(f"Stage 22 : Source a Ingested:   rows out:{len(source_b)}")
    logger.info("=" * 50)
    

    logger.info("STAGE 3: Cleaning Source A....")
    clean_prices, decisions = clean_data()
    logger.info(f"Stage 33 : Source a Ingested  rows out:{len(source_a)}"
                f"rows out: {len(clean_prices)}"
                f"Decisions  : {len(decisions)} ")
    logger.info("=" * 50)

    #logger.info("STAGE 4: Validat")
    #negative_rain = rule_negative_rain(source_b_df)

    #if len(negative_rain) > 0:
       # raise ValueError(
        #    f"Source B contains {len(negative_rain)} negative rainfall records."
        #)

    #logger.info(
       # "Rainfall validation passed: %d negative records",
       # len(negative_rain)
    #)

    logger.info("STAGE 4: Merging price and rainfall data")
    merged = merge_data(clean_prices, source_b)
    logger.info(f"Stage 4:Merge complete: rows in: {len(clean_prices)},rows out: {len(merged)}")
    logger.info("=" * 50)

    

    logger.info(
        "Stored merged dataset: %s",
        merged_data_path
    )
    logger.info("Stage 5: Saving merged file")
    merged.to_parquet(
           PATH,
            index=False
    ) 
    
    logger.info(
        f"Stage 55:Saving Complete:Saved {len(merged)}",
        )
    logger.info("=" * 50)
    
    logger.info("====PIPELINE RUN COMPLETED SUCCESSFULLY===")
    return

if __name__ == "__main__":
    run_pipe()