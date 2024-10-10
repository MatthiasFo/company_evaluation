with current_and_last_revenues as (
    select
        id,
        total_revenue,
        lag(total_revenue) over (partition by ticker order by end_of_period) as last_revenue
    from {{ ref( 'stg_yahoo_income_stmts_yearly' ) }}
),

revenue_growths as (
    select
        id,
        (total_revenue - last_revenue) / last_revenue as revenue_growth
    from current_and_last_revenues
    where last_revenue > 0
),

current_and_last_shares as (
    select
        id,
        outstanding_shares as current_shares,
        lag(outstanding_shares) over (partition by ticker order by end_of_period) as last_shares
    from {{ ref( 'stg_yahoo_balance_sheets_yearly' ) }}
),

share_growths as (
    select
        id,
        (current_shares - last_shares) / last_shares as shares_growth
    from current_and_last_shares
    where last_shares > 0
),

combined_filings as (
    select
        income_stmts.ticker,
        income_stmts.end_of_period,
        income_stmts.total_revenue,
        income_stmts.net_income,
        income_stmts.cost_of_goods_sold,
        income_stmts.selling_general_and_administration,
        cashflows.free_cash_flow,
        balance_sheets.stockholders_equity,
        balance_sheets.total_assets,
        balance_sheets.accounts_receivable,
        balance_sheets.cash_and_cash_equivalents,
        balance_sheets.current_assets,
        balance_sheets.current_liabilities,
        balance_sheets.inventory,
        balance_sheets.long_term_debt,
        rev_growths.revenue_growth,
        share_growths.shares_growth,
        coalesce(cashflows.dividends_paid, income_stmts.preferred_stock_dividends) as dividends_paid,
        -- make it compatible with the FMP filings
        extract(year from income_stmts.end_of_period) || '_FY_' || income_stmts.ticker as filing_id
    from {{ ref( 'stg_yahoo_income_stmts_yearly' ) }} as income_stmts
    inner join {{ ref( 'stg_yahoo_cashflows_yearly' ) }} as cashflows on income_stmts.id = cashflows.id
    inner join
        {{ ref( 'stg_yahoo_balance_sheets_yearly' ) }} as balance_sheets
        on income_stmts.id = balance_sheets.id
    left join revenue_growths as rev_growths on income_stmts.id = rev_growths.id
    left join share_growths as share_growths on income_stmts.id = share_growths.id
)

select * from combined_filings
