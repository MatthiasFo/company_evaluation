with source_data as (
    select
        id,
        symbol as ticker,
        requesttimestamp as request_timestamp,
        sharesoutstanding as shares_outstanding,
        eps as earnings_per_share,
        pe as price_earnings_ratio
    from {{ source('financial_modeling_prep', 'quote') }}
)

select *
from source_data
