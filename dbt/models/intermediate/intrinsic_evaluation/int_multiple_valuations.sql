with combined_data as (
    select
        cf.filing_id,
        cf.ticker,
        cf.end_of_period,
        cc.country,
        cc.sector,
        cf.total_revenue,
        cf.net_income,
        cf.free_cash_flow,
        cf.stockholders_equity,
        cf.total_assets,
        cf.long_term_debt,
        cf.cash_and_cash_equivalents,
        cc.market_cap,
        cc.current_price,
        cc.shares_outstanding,
        cc.price_earnings_ratio,
        dcf.normal as dcf_valuation_normal_conditions
    from {{ ref('int_combined_financial_filings') }} as cf
    inner join {{ ref('int_current_company_infos') }} as cc
        on cf.ticker = cc.ticker
    left join {{ source('dcf_model', 'dcf_model_evaluations') }} as dcf
        on cf.ticker = dcf.ticker
    where cf.total_revenue > 0
        and cf.stockholders_equity > 0
        and cc.shares_outstanding > 0
        and cc.current_price > 0
),

ratios as (
    select
        filing_id,
        ticker,
        end_of_period,
        country,
        sector,
        -- Price to Sales Ratio (Total Revenue per Share over Current Price)
        (total_revenue / nullif(shares_outstanding, 0)) / nullif(current_price, 0) as price_to_sales_ratio,
        -- Price to Book Ratio
        current_price / nullif(stockholders_equity / nullif(shares_outstanding, 0), 0) as price_to_book_ratio,
        -- price to DCF evaluation
        current_price / nullif(dcf_valuation_normal_conditions, 0) as price_to_dcf_normal_evaluation,
        -- price earnings ratio
        case
            when price_earnings_ratio > 0 then price_earnings_ratio
            when net_income > 0 then current_price / (net_income / shares_outstanding)
        end as price_earnings_ratio,
        -- Earnings Yield
        case
            when price_earnings_ratio > 0 then 1 / price_earnings_ratio else
                (net_income / shares_outstanding) / current_price
        end as earnings_yield,
        -- Cash Return
        free_cash_flow / nullif(market_cap + long_term_debt - cash_and_cash_equivalents, 0) as cash_return

    from combined_data
)

select
    filing_id,
    ticker,
    end_of_period,
    country,
    sector,
    price_to_sales_ratio,
    price_to_book_ratio,
    price_to_dcf_normal_evaluation,
    price_earnings_ratio,
    earnings_yield,
    cash_return
from ratios
