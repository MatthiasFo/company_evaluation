with source_data as (
    select
        id,
        symbol as ticker,
        revenue as total_revenue,
        netincome as net_income,
        costofrevenue as cost_of_goods_sold,
        sellinggeneralandadministrativeexpenses as selling_general_and_administration,
        date(calendaryear, 12, 31) as end_of_period
    from {{ source('financial_modeling_prep', 'income_stmt') }}
)

select *
from source_data
