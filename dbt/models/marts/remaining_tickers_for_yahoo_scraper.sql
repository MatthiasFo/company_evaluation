with us_and_non_us_stocks as (
    select *
    from {{ ref('stg_fmp_api_available_us_stocks') }}
    union all
    select *
    from {{ ref('stg_fmp_api_available_non_us_stocks') }}
)

select ticker
from us_and_non_us_stocks
where ticker not in (select ticker from {{ ref('int_already_scraped_symbols') }})
