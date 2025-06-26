from typing import List

import polars as pl


@transformer
def transform_data(data: pl.DataFrame, *args, **kwargs) -> List[pl.DataFrame]:
    """
    Transforms each chunk by adding 'risk_score' based on 'cardiac_risk_score'.
    """
    def assign_risk_score(score):
        if not score or score == '':
            return 'No score'
        
        try:
            score = float(score)
            if score < 5:
                return 'High risk'
            elif 5 <= score <= 7:
                return 'Medium risk'
            elif score > 7:
                return 'Low risk'
            else:
                return 'Unknown'
        except ValueError:
            return 'Invalid score'

    data = data.with_columns([
        pl.when(pl.col('cardiac_risk_score').is_null())
        .then('No score')
        .otherwise(
            pl.col('cardiac_risk_score')
            .cast(pl.Utf8)
            .map_elements(assign_risk_score)
        )
        .alias('risk_score')
    ])

    return data