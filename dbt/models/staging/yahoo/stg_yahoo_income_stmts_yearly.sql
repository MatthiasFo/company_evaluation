with source_data as (
    select
        id,
        ticker,
        country,
        industry,
        end_of_period,
        total_revenue,
        net_income,
        cost_of_revenue as cost_of_goods_sold,
        preferred_stock_dividends,
        coalesce(
            selling_general_and_administration,
            general_and_administrative_expense + selling_and_marketing_expense
        ) as selling_general_and_administration
    from {{ source('yahoo_finance', 'income_statement_yearly') }}
)

select *
from source_data
