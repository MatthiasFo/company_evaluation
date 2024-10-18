with moat as (
    select
        filing_id,
        ticker,
        country,
        sector,
        end_of_period,
        case when return_on_assets >= 0.06 then 1 else 0 end as moat_roa,
        case when return_on_equity >= 0.15 then 1 else 0 end as moat_roe,
        case when net_margin_over_revenue >= 0.15 then 1 else 0 end as moat_net_margin,
        case when free_cash_flow_over_revenue >= 0.05 then 1 else 0 end as moat_free_cash_flow
    from {{ ref('int_fundamental_ratios') }}
)

select
    filing_id,
    ticker,
    country,
    sector,
    end_of_period,
    moat_roa + moat_roe + moat_net_margin + moat_free_cash_flow as moat_score
from moat
