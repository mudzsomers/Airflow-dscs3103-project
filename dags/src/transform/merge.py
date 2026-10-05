def merge_data(clean ,rainfall_df) :
    merged=clean.merge(rainfall_df,
                    on=["market","date"],
                    how="inner"
                    )
    return merged