with source_data as (
    select
        id,
        symbol as ticker,
        totalrevenue as total_revenue,
        netincome as net_income,
        costofrevenue as cost_of_goods_sold,
        sellinggeneralandadministrative as selling_general_and_administration,
        fiscaldateending as end_of_period
    from {{ source('alphavantage', 'income_stmts_annually') }}
)

select *
from source_data
