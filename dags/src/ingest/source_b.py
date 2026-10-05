

import os
import requests
import pandas as pd
import time

from src.common.config import (
    MARKET_COORDS,
    SOURCE_B_RAW_PATH,
    RAINFALL_URL,
    RAINFALL_END_DATE,
    RAINFALL_START_DATE,
    


)

def  get_mkt_rainfall(mkt_name,latitude,longitude,start_date=RAINFALL_START_DATE, end_date=RAINFALL_END_DATE):


    params={ 
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "daily" : "precipitation_sum"

    }
    response =requests.get(RAINFALL_URL, params=params,timeout=10)
    if response.status_code !=200:
        raise RuntimeError(
             f"Failed to get data for {mkt_name} : status{response.status_code}"
        )
    daily=response.json()["daily"]
    return pd.DataFrame({
        #"date":daily["time"],
        "date": daily["time"],
        "market":mkt_name,
        "rainfall": daily["precipitation_sum"]


    })

def get_all_mkt_rain():
    """Fetches rainfall data for every market and combines it into one dataframe."""
    all_rainfall = []

    for mkt_name, (latitude, longitude) in MARKET_COORDS.items():
        mkt_df = get_mkt_rainfall(mkt_name, latitude, longitude)
        all_rainfall.append(mkt_df)
        time.sleep(5)

    rainfall_df = pd.concat(all_rainfall, ignore_index=True)
    #rainfall_df.to_csv(SOURCE_B_RAW_PATH, index=False)
    return rainfall_df


def ingest_source_b(path=SOURCE_B_RAW_PATH):
    if os.path.exists(path):
        return pd.read_csv(path)
    df_b = get_all_mkt_rain()
    df_b.to_csv(path,index=False)
    return df_b









##CODE BELOW IS WHAT MR.BRIAN WROTE IN CLASS.(AS COMPARED TO THE CODE ABOVE WHICH I WROTE)##
'''def get_all_mkt_rain():
    all_mkt_rain = []

    for mkt_names, (latitude, longitude) in MARKET_COORDS.items():
        rainfall = get_mkt_rainfall(
            mkt_names,
            latitude,
            longitude
        )
        all_mkt_rain.append(rainfall)
        time.sleep(5)

    return pd.concat(all_mkt_rain, ignore_index=True)

def ingest_source_b(path=source_b_raw_path):
    if os.path.exists(path):
        return pd.read_csv(path)

    df_b = get_all_mkt_rain()
    df_b.to_csv(path, index=False)
    return df_b'''

if __name__ == "__main__":
    df = ingest_source_b()

    print(df.head())
    print("\nNumber of rows:", len(df))
    print("\nMarkets:")
    print(df["market"].unique())
    print("\nRows per market:")
    print(df["market"].value_counts())

    

