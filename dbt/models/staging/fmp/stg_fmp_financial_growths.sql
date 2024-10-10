with source_data as (
    select
        id,
        symbol as ticker,
        requesttimestamp as request_timestamp,
        revenuegrowth as revenue_growth,
        weightedaveragesharesdilutedgrowth as weighted_average_shares_diluted_growth,
        date(calendaryear, 12, 31) as end_of_period
    from {{ source('financial_modeling_prep', 'financial_growth') }}
)

select *
from source_data
