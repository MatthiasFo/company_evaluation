with base as (
    select
        ticker,
        max(sector) as sector,
        max(country) as country,
        avg(net_margin_over_revenue) as avg_net_margin_over_revenue,
        avg(free_cash_flow_over_revenue) as avg_free_cash_flow_over_revenue,
        avg(return_on_assets) as avg_return_on_assets,
        avg(return_on_equity) as avg_return_on_equity,
        avg(asset_turnover_ratio) as avg_asset_turnover_ratio,
        avg(inventory_turnover_ratio) as avg_inventory_turnover_ratio,
        avg(inventory_over_revenue) as avg_inventory_over_revenue,
        avg(sga_over_revenue) as avg_sga_over_revenue,
        avg(current_ratio) as avg_current_ratio,
        avg(quick_ratio) as avg_quick_ratio,
        avg(fin_leverage) as avg_fin_leverage,
        avg(accounts_receivable_over_revenue) as avg_accounts_receivable_over_revenue
    from {{ ref('int_fundamental_ratios') }}
    where end_of_period > date_sub(current_date(), interval 5 year)
    group by ticker
),

competition as (
    select
        sector,
        country,
        avg(net_margin_over_revenue) as comp_net_margin_over_revenue,
        avg(free_cash_flow_over_revenue) as comp_free_cash_flow_over_revenue,
        avg(return_on_assets) as comp_return_on_assets,
        avg(return_on_equity) as comp_return_on_equity,
        avg(asset_turnover_ratio) as comp_asset_turnover_ratio,
        avg(inventory_turnover_ratio) as comp_inventory_turnover_ratio,
        avg(inventory_over_revenue) as comp_inventory_over_revenue,
        avg(sga_over_revenue) as comp_sga_over_revenue,
        avg(current_ratio) as comp_current_ratio,
        avg(quick_ratio) as comp_quick_ratio,
        avg(fin_leverage) as comp_fin_leverage,
        avg(accounts_receivable_over_revenue) as comp_accounts_receivable_over_revenue
    from {{ ref('int_fundamental_ratios') }}
    where end_of_period > date_sub(current_date(), interval 5 year)
    group by sector, country
),

final_scores as (
    select
        b.ticker,
        b.sector,
        b.country,
        b.avg_net_margin_over_revenue,
        b.avg_free_cash_flow_over_revenue,
        b.avg_return_on_assets,
        b.avg_return_on_equity,
        b.avg_asset_turnover_ratio,
        b.avg_inventory_turnover_ratio,
        b.avg_inventory_over_revenue,
        b.avg_sga_over_revenue,
        b.avg_current_ratio,
        b.avg_quick_ratio,
        b.avg_fin_leverage,
        b.avg_accounts_receivable_over_revenue,
        c.comp_net_margin_over_revenue,
        c.comp_free_cash_flow_over_revenue,
        c.comp_return_on_assets,
        c.comp_return_on_equity,
        c.comp_asset_turnover_ratio,
        c.comp_inventory_turnover_ratio,
        c.comp_inventory_over_revenue,
        c.comp_sga_over_revenue,
        c.comp_current_ratio,
        c.comp_quick_ratio,
        c.comp_fin_leverage,
        c.comp_accounts_receivable_over_revenue,
        -- Calculate the final score based on the comparison
        (
            case
                when b.avg_net_margin_over_revenue > c.comp_net_margin_over_revenue then 1 else 0
            end
            + case
                when b.avg_free_cash_flow_over_revenue > c.comp_free_cash_flow_over_revenue then 1 else 0
            end
            + case
                when b.avg_return_on_assets > c.comp_return_on_assets then 1 else 0
            end
            + case
                when b.avg_return_on_equity > c.comp_return_on_equity then 1 else 0
            end
            + case
                when b.avg_asset_turnover_ratio > c.comp_asset_turnover_ratio then 1 else 0
            end
            + case
                when b.avg_inventory_turnover_ratio > c.comp_inventory_turnover_ratio then 1 else 0
            end
            + case
                when b.avg_inventory_over_revenue < c.comp_inventory_over_revenue then 1 else 0
            end
            + case
                when b.avg_sga_over_revenue < c.comp_sga_over_revenue then 1 else 0
            end
            + case
                when b.avg_current_ratio > c.comp_current_ratio then 1 else 0
            end
            + case
                when b.avg_quick_ratio > c.comp_quick_ratio then 1 else 0
            end
            + case
                when b.avg_fin_leverage < c.comp_fin_leverage then 1 else 0
            end
            + case
                when b.avg_accounts_receivable_over_revenue < c.comp_accounts_receivable_over_revenue then 1 else 0
            end
        ) as final_score
    from base as b
    inner join competition as c on b.sector = c.sector and b.country = c.country
)

select * from final_scores
