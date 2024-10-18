with combined_filings as (
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
        balance_sheets.outstanding_shares,
        cashflows.dividends_paid,
        -- make it compatible with the FMP filings
        extract(year from income_stmts.end_of_period) || '_FY_' || income_stmts.ticker as filing_id
    from {{ ref( 'stg_alphavantage_income_stmts' ) }} as income_stmts
    inner join {{ ref( 'stg_alphavantage_cashflows' ) }} as cashflows on income_stmts.id = cashflows.id
    inner join
        {{ ref( 'stg_alphavantage_balance_sheets' ) }} as balance_sheets
        on income_stmts.id = balance_sheets.id
)

select * from combined_filings
