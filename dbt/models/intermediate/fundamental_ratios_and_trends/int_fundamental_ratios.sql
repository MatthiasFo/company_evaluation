with base as (
    select
        filing.filing_id,
        filing.ticker,
        filing.end_of_period,
        info.sector,
        info.country,
        filing.total_revenue,
        filing.net_income,
        filing.cost_of_goods_sold,
        filing.selling_general_and_administration,
        filing.free_cash_flow,
        filing.dividends_paid,
        filing.stockholders_equity,
        filing.total_assets,
        filing.accounts_receivable,
        filing.cash_and_cash_equivalents,
        filing.current_assets,
        filing.current_liabilities,
        filing.inventory,
        filing.long_term_debt,
        filing.outstanding_shares
    from {{ ref('int_combined_financial_filings') }} as filing
    left join {{ ref('int_current_company_infos') }} as info on filing.ticker = info.ticker
    where total_revenue > 0
        and stockholders_equity > 0
-- total assets could be null 
-- inventory could be null
-- current_liabilities could be null
)

select
    filing_id,
    ticker,
    end_of_period,
    country,
    sector,
    -- Profitability Ratios
    net_income / total_revenue as net_margin_over_revenue,
    free_cash_flow / total_revenue as free_cash_flow_over_revenue,
    net_income / nullif(total_assets, 0) as return_on_assets,
    net_income / stockholders_equity as return_on_equity,

    -- Efficiency Ratios
    total_revenue / nullif(total_assets, 0) as asset_turnover_ratio,
    cost_of_goods_sold / nullif(inventory, 0) as inventory_turnover_ratio,
    inventory / total_revenue as inventory_over_revenue,
    selling_general_and_administration / total_revenue as sga_over_revenue,

    -- Financial Health Ratios
    current_assets / nullif(current_liabilities, 0) as current_ratio,
    (current_assets - inventory) / nullif(current_liabilities, 0) as quick_ratio,
    total_assets / stockholders_equity as fin_leverage,

    -- Management Ratios
    accounts_receivable / total_revenue as accounts_receivable_over_revenue

from base
