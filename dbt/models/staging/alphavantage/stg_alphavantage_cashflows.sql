with source_data as (
    select
        id,
        symbol as ticker,
        dividendpayout as dividends_paid,
        dividendpayoutcommonstock as dividend_payout_common_stock,
        dividendpayoutpreferredstock as dividend_payout_preferred_stock,
        fiscaldateending as end_of_period,
        operatingcashflow - capitalexpenditures as free_cash_flow
    from {{ source('alphavantage', 'cashflows_annually') }}
)

select *
from source_data
