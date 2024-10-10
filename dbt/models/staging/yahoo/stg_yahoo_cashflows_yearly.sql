with source_data as (
    select
        id,
        ticker,
        country,
        industry,
        end_of_period,
        free_cash_flow,
        coalesce(cash_dividends_paid, common_stock_dividend_paid) as dividends_paid
    from {{ source('yahoo_finance', 'cash_flow_yearly') }}
)

select *
from source_data
