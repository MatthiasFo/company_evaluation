with source_data as (
    select
        id,
        symbol as ticker,
        companyname as company_name,
        sector,
        industry,
        price as current_price,
        mktcap as market_cap,
        requesttimestamp as request_timestamp,
        case when country = "US" then "United States" else country end as country
    from {{ source('financial_modeling_prep', 'profile') }}
)

select *
from source_data
