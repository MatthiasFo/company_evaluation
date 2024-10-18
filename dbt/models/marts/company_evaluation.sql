-- This gives us all the ratios, trends and multiples of the company as averages over the period (remove the "avg_" prefix for easier readability)
-- it also gives us the current price and basic information
-- it also includes the DCF evaluation with the various scenarios

-- It does not give us any time series data but we do not need this when we are just checking for the top 5 companies to look at
-- Detailed time series investigations need to be done with another model

-- Make this a table because it is used in the dashboards
{{ config(materialized='table') }}


with current_info as (
    select *
    from {{ ref('int_current_company_infos') }}
),

comparative_ratios as (
    select *
    from {{ ref('int_comparative_ratios') }}
),

comparative_multiples as (
    select *
    from {{ ref('int_comparative_multiples') }}
),

comparative_trends as (
    select *
    from {{ ref('int_comparative_trends') }}
),

comparative_guideline as (
    select *
    from {{ ref('int_comparative_guideline_scores') }}
),

dcf_data as (
    select *
    from {{ source('dcf_model', 'dcf_model_evaluations') }}
),

final as (
    select
        ci.ticker,
        ci.company_name,
        ci.country,
        ci.industry,
        ci.sector,
        ci.current_price,
        ci.market_cap,
        ci.shares_outstanding,
        ci.earnings_per_share,

        cr.avg_net_margin_over_revenue as net_margin_over_revenue,
        cr.avg_free_cash_flow_over_revenue as free_cash_flow_over_revenue,
        cr.avg_return_on_assets as return_on_assets,
        cr.avg_return_on_equity as return_on_equity,
        cr.avg_asset_turnover_ratio as asset_turnover_ratio,
        cr.avg_inventory_turnover_ratio as inventory_turnover_ratio,
        cr.avg_inventory_over_revenue as inventory_over_revenue,
        cr.avg_sga_over_revenue as sga_over_revenue,
        cr.avg_current_ratio as current_ratio,
        cr.avg_quick_ratio as quick_ratio,
        cr.avg_fin_leverage as fin_leverage,
        cr.avg_accounts_receivable_over_revenue as accounts_receivable_over_revenue,
        cr.comp_net_margin_over_revenue,
        cr.comp_free_cash_flow_over_revenue,
        cr.comp_return_on_assets,
        cr.comp_return_on_equity,
        cr.comp_asset_turnover_ratio,
        cr.comp_inventory_turnover_ratio,
        cr.comp_inventory_over_revenue,
        cr.comp_sga_over_revenue,
        cr.comp_current_ratio,
        cr.comp_quick_ratio,
        cr.comp_fin_leverage,
        cr.comp_accounts_receivable_over_revenue,
        cr.final_score as comparative_ratios_score,

        cm.avg_price_earnings_ratio as price_earnings_ratio,
        cm.avg_price_to_sales_ratio as price_to_sales_ratio,
        cm.avg_price_to_book_ratio as price_to_book_ratio,
        cm.avg_price_to_dcf_normal_evaluation as price_to_dcf_normal_evaluation,
        cm.avg_earnings_yield as earnings_yield,
        cm.avg_cash_return as cash_return,
        cm.comp_price_earnings_ratio,
        cm.comp_price_to_sales_ratio,
        cm.comp_price_to_book_ratio,
        cm.comp_price_to_dcf_normal_evaluation,
        cm.comp_earnings_yield,
        cm.comp_cash_return,
        cm.final_score as comparative_multiples_score,

        ct.avg_revenue_growth as revenue_growth,
        ct.avg_shares_growth as shares_growth,
        ct.avg_sga_over_revenue_change as sga_over_revenue_change,
        ct.avg_inventory_over_revenue_change as inventory_over_revenue_change,
        ct.avg_accounts_receivable_over_revenue_change as accounts_receivable_over_revenue_change,
        ct.comp_revenue_growth,
        ct.comp_shares_growth,
        ct.comp_sga_over_revenue_change,
        ct.comp_inventory_over_revenue_change,
        ct.comp_accounts_receivable_over_revenue_change,
        ct.final_score as comparative_trends_score,

        cg.avg_moat_score as moat_score,
        cg.avg_financial_health_score as financial_health_score,
        cg.avg_efficiency_score as efficiency_score,
        cg.avg_management_score as management_score,
        cg.avg_total_score as guideline_total_score,
        cg.comp_moat_score,
        cg.comp_financial_health_score,
        cg.comp_efficiency_score,
        cg.comp_management_score,
        cg.comp_total_score,
        cg.final_score as comparative_guideline_score,

        dcf.normal as dcf_normal_evaluation,
        dcf.stable as dcf_stable_evaluation,
        dcf.stable_and_strong_growth as dcf_stable_and_strong_growth_evaluation,
        dcf.volatile as dcf_volatile_evaluation,
        dcf.volatile_and_weak_growth as dcf_volatile_and_weak_growth_evaluation,

        (cr.final_score + cm.final_score + ct.final_score + cg.final_score) as total_score
    from current_info as ci
    left join comparative_ratios as cr on ci.ticker = cr.ticker
    left join comparative_multiples as cm on ci.ticker = cm.ticker
    left join comparative_trends as ct on ci.ticker = ct.ticker
    left join comparative_guideline as cg on ci.ticker = cg.ticker
    left join dcf_data as dcf on ci.ticker = dcf.ticker
    where ci.country is not null
        and ci.industry is not null
        and ci.sector is not null
        and ci.company_name is not null
)

select * from final
