with cashflow as (
    select
        ticker,
        max(end_of_period) as last_end_of_period,
        avg(free_cash_flow) as free_cash_flow
    from {{ ref('int_combined_financial_filings') }}
    where end_of_period > date_sub(current_date(), interval 10 year)
    group by ticker
),

rev_growth as (
    select
        ticker,
        avg(revenue_growth) as revenue_growth
    from {{ ref('int_fundamental_trends') }}
    where end_of_period > date_sub(current_date(), interval 10 year)
    group by ticker
),

current_data as (
    select
        id,
        ticker,
        shares_outstanding
    from {{ ref('int_current_company_infos') }}
)

select
    current_data.id,
    current_data.ticker,
    current_data.shares_outstanding,
    rev_growth.revenue_growth,
    cashflow.free_cash_flow
from current_data
inner join rev_growth on current_data.ticker = rev_growth.ticker
inner join cashflow on current_data.ticker = cashflow.ticker
where cashflow.free_cash_flow is not null
    and rev_growth.revenue_growth is not null
    and current_data.shares_outstanding is not null
    and (
        current_data.ticker not in (select ticker from {{ source('dcf_model', 'dcf_model_evaluations') }})
        or cashflow.last_end_of_period < date_sub(current_date(), interval 1 year)
    )
