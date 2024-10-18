with management as (
    select
        filing_id,
        ticker,
        country,
        sector,
        end_of_period,
        case when accounts_receivable_over_revenue_change <= 0 then 1 else 0 end as management_ar,
        case when shares_growth <= 0.02 then 1 else 0 end as management_shares_growth
    from {{ ref('int_fundamental_trends') }}
)

select
    filing_id,
    ticker,
    country,
    sector,
    end_of_period,
    management_ar + management_shares_growth as management_score
from management
