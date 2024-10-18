with base as (
    select
        ticker,
        max(sector) as sector,
        max(country) as country,
        avg(revenue_growth) as avg_revenue_growth,
        avg(shares_growth) as avg_shares_growth,
        avg(sga_over_revenue_change) as avg_sga_over_revenue_change,
        avg(inventory_over_revenue_change) as avg_inventory_over_revenue_change,
        avg(accounts_receivable_over_revenue_change) as avg_accounts_receivable_over_revenue_change
    from {{ ref('int_fundamental_trends') }}
    group by ticker
),

competition as (
    select
        sector,
        country,
        avg(revenue_growth) as comp_revenue_growth,
        avg(shares_growth) as comp_shares_growth,
        avg(sga_over_revenue_change) as comp_sga_over_revenue_change,
        avg(inventory_over_revenue_change) as comp_inventory_over_revenue_change,
        avg(accounts_receivable_over_revenue_change) as comp_accounts_receivable_over_revenue_change
    from {{ ref('int_fundamental_trends') }}
    group by sector, country
),

comparison as (
    select
        b.ticker,
        b.sector,
        b.country,
        b.avg_revenue_growth,
        b.avg_shares_growth,
        b.avg_sga_over_revenue_change,
        b.avg_inventory_over_revenue_change,
        b.avg_accounts_receivable_over_revenue_change,
        c.comp_revenue_growth,
        c.comp_shares_growth,
        c.comp_sga_over_revenue_change,
        c.comp_inventory_over_revenue_change,
        c.comp_accounts_receivable_over_revenue_change,
        case
            when b.avg_revenue_growth > c.comp_revenue_growth then 1 else 0
        end as revenue_growth_comparison,
        case
            when b.avg_shares_growth < c.comp_shares_growth then 1 else 0
        end as shares_growth_comparison,
        case
            when b.avg_sga_over_revenue_change < c.comp_sga_over_revenue_change then 1 else 0
        end as sga_over_revenue_change_comparison,
        case
            when b.avg_inventory_over_revenue_change < c.comp_inventory_over_revenue_change then 1 else 0
        end as inventory_over_revenue_change_comparison,
        case
            when
                b.avg_accounts_receivable_over_revenue_change < c.comp_accounts_receivable_over_revenue_change
                then 1
            else 0
        end as accounts_receivable_over_revenue_change_comparison
    from base as b
    inner join competition as c on b.sector = c.sector and b.country = c.country
),

final_score as (
    select
        ticker,
        sector,
        country,
        avg_revenue_growth,
        avg_shares_growth,
        avg_sga_over_revenue_change,
        avg_inventory_over_revenue_change,
        avg_accounts_receivable_over_revenue_change,
        comp_revenue_growth,
        comp_shares_growth,
        comp_sga_over_revenue_change,
        comp_inventory_over_revenue_change,
        comp_accounts_receivable_over_revenue_change,
        revenue_growth_comparison
        + shares_growth_comparison
        + sga_over_revenue_change_comparison
        + inventory_over_revenue_change_comparison
        + accounts_receivable_over_revenue_change_comparison as final_score
    from comparison
)

select *
from final_score
