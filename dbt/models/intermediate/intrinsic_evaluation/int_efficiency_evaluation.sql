with efficiency as (
    select
        filing_id,
        ticker,
        country,
        sector,
        end_of_period,
        -- when sga_over_revenue <= sga_over_revenue_competition then 1 else 0 end as efficiency_sga,
        case when sga_over_revenue_change <= 0 then 1 else 0 end as efficiency_sga_change,
        case when inventory_over_revenue_change <= 0 then 1 else 0 end as efficiency_inventory_change
    from {{ ref('int_fundamental_trends') }}
)

select
    filing_id,
    ticker,
    country,
    sector,
    end_of_period,
    efficiency_sga_change + efficiency_inventory_change as efficiency_score
from efficiency
