with financial_health as (
    select
        filing_id,
        ticker,
        country,
        sector,
        end_of_period,
        case when sector != 'Financial Services' and current_ratio >= 1.5 then 1 else 0 end as health_current_ratio,
        case when sector != 'Financial Services' and quick_ratio >= 1.0 then 1 else 0 end as health_quick_ratio,
        case when sector != 'Financial Services' and fin_leverage <= 4.0 then 1 else 0 end as health_fin_leverage
    from {{ ref('int_fundamental_ratios') }}
)

select
    filing_id,
    ticker,
    country,
    sector,
    end_of_period,
    health_current_ratio + health_quick_ratio + health_fin_leverage as financial_health_score
from financial_health
