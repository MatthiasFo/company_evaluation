with source_data as (
    select
        id,
        symbol as ticker,
        freecashflow as free_cash_flow,
        dividendspaid as dividends_paid,
        date(calendaryear, 12, 31) as end_of_period
    from {{ source('financial_modeling_prep', 'cashflow') }}
)

select *
from source_data
