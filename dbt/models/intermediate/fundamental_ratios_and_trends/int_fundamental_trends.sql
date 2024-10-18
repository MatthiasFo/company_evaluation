with revenue_growths as (
    select
        filing_id,
        ticker,
        total_revenue,
        end_of_period,
        lag(total_revenue) over (partition by ticker order by end_of_period) as last_revenue
    from {{ ref('int_combined_financial_filings') }}
),

share_growths as (
    select
        filing_id,
        outstanding_shares as current_shares,
        lag(outstanding_shares) over (partition by ticker order by end_of_period) as last_shares
    from {{ ref('int_combined_financial_filings') }}  -- Assuming shares data is available in the combined filings
),

combined_growths as (
    select
        rev.filing_id,
        rev.ticker,
        rev.end_of_period,
        (rev.total_revenue - rev.last_revenue) / rev.last_revenue as revenue_growth,
        (sh.current_shares - sh.last_shares) / sh.last_shares as shares_growth
    from revenue_growths as rev
    inner join share_growths as sh on rev.filing_id = sh.filing_id
    where rev.last_revenue > 0 and sh.last_shares > 0
),

trend_calculations as (
    select
        rev.filing_id,
        rev.ticker,
        rev.end_of_period,
        ratios.country,
        ratios.sector,
        (rev.total_revenue - rev.last_revenue) / rev.last_revenue as revenue_growth,
        (sh.current_shares - sh.last_shares) / sh.last_shares as shares_growth,
        -- Assuming you have the necessary columns in your ratios table
        (
            ratios.sga_over_revenue
            - lag(ratios.sga_over_revenue) over (partition by rev.ticker order by rev.end_of_period)
        ) as sga_over_revenue_change,
        (
            ratios.inventory_over_revenue
            - lag(ratios.inventory_over_revenue) over (partition by rev.ticker order by rev.end_of_period)
        ) as inventory_over_revenue_change,
        (
            ratios.accounts_receivable_over_revenue
            - lag(ratios.accounts_receivable_over_revenue) over (partition by rev.ticker order by rev.end_of_period)
        ) as accounts_receivable_over_revenue_change
    from revenue_growths as rev
    inner join share_growths as sh on rev.filing_id = sh.filing_id
    left join
        {{ ref('int_fundamental_ratios') }} as ratios
        on rev.filing_id = ratios.filing_id
    where rev.last_revenue > 0 and sh.last_shares > 0

)

select
    filing_id,
    ticker,
    end_of_period,
    country,
    sector,
    revenue_growth,
    shares_growth,
    sga_over_revenue_change,
    inventory_over_revenue_change,
    accounts_receivable_over_revenue_change
from trend_calculations
