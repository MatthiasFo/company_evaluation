with combined_filings as (
    -- must specify the columns to avoid big query from running into datatype error
    select
        filing_id,
        ticker,
        end_of_period,
        total_revenue,
        net_income,
        cost_of_goods_sold,
        selling_general_and_administration,
        free_cash_flow,
        dividends_paid,
        stockholders_equity,
        total_assets,
        accounts_receivable,
        cash_and_cash_equivalents,
        current_assets,
        current_liabilities,
        inventory,
        long_term_debt,
        revenue_growth,
        shares_growth
    from {{ ref('int_fmp_combined_filings') }}
    union all
    select
        filing_id,
        ticker,
        end_of_period,
        total_revenue,
        net_income,
        cost_of_goods_sold,
        selling_general_and_administration,
        free_cash_flow,
        dividends_paid,
        stockholders_equity,
        total_assets,
        accounts_receivable,
        cash_and_cash_equivalents,
        current_assets,
        current_liabilities,
        inventory,
        long_term_debt,
        revenue_growth,
        shares_growth
    from {{ ref('int_alphavantage_combined_filings') }}
    union all
    select
        filing_id,
        ticker,
        end_of_period,
        total_revenue,
        net_income,
        cost_of_goods_sold,
        selling_general_and_administration,
        free_cash_flow,
        dividends_paid,
        stockholders_equity,
        total_assets,
        accounts_receivable,
        cash_and_cash_equivalents,
        current_assets,
        current_liabilities,
        inventory,
        long_term_debt,
        revenue_growth,
        shares_growth
    from {{ ref('int_yahoo_filings_annually') }}
-- disregard quarterly filings as they rarely provide additional information (to often it is only a single quarter)
),

combined_filings_with_row_number_for_deduplication as (
    select
        *,
        row_number() over (partition by filing_id order by end_of_period desc) as rn
    from combined_filings
)

select
    filing_id,
    ticker,
    end_of_period,
    total_revenue,
    net_income,
    cost_of_goods_sold,
    selling_general_and_administration,
    free_cash_flow,
    dividends_paid,
    stockholders_equity,
    total_assets,
    accounts_receivable,
    cash_and_cash_equivalents,
    current_assets,
    current_liabilities,
    inventory,
    long_term_debt,
    revenue_growth,
    shares_growth
from combined_filings_with_row_number_for_deduplication
where rn = 1
    and total_revenue > 0 -- with 0 or null revenue we cannot calculate ratios
    and (inventory > 0 or inventory is null) -- cannot handle negative inventory
    and free_cash_flow is not null -- free cash flow is important for the discounted cashflow model
    and (dividends_paid is null or dividends_paid <= 0) -- dividends paid must be negative or null
    and (accounts_receivable is null or accounts_receivable >= 0) -- accounts receivable must be positive or null
    -- cash and cash equivalents must be positive or null
    and (cash_and_cash_equivalents is null or cash_and_cash_equivalents >= 0)
    and (stockholders_equity is null or stockholders_equity >= 0) -- stockholders equity must be positive or null
    and (long_term_debt is null or long_term_debt >= 0)
