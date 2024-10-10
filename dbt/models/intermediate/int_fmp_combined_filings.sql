with combined_filings as (
    select
        income_stmts.id as filing_id,
        income_stmts.ticker,
        income_stmts.end_of_period,
        income_stmts.total_revenue,
        income_stmts.net_income,
        income_stmts.cost_of_goods_sold,
        income_stmts.selling_general_and_administration,
        cashflows.free_cash_flow,
        cashflows.dividends_paid,
        balance_sheets.stockholders_equity,
        balance_sheets.total_assets,
        balance_sheets.accounts_receivable,
        balance_sheets.cash_and_cash_equivalents,
        balance_sheets.current_assets,
        balance_sheets.current_liabilities,
        balance_sheets.inventory,
        balance_sheets.long_term_debt,
        growths.revenue_growth,
        growths.weighted_average_shares_diluted_growth as shares_growth
    from {{ ref( 'stg_fmp_income_stmts' ) }} as income_stmts
    inner join {{ ref( 'stg_fmp_cashflows' ) }} as cashflows on income_stmts.id = cashflows.id
    inner join {{ ref( 'stg_fmp_balance_sheets' ) }} as balance_sheets on income_stmts.id = balance_sheets.id
    inner join {{ref('stg_fmp_financial_growths')}} as growths on income_stmts.id = growths.id
)

select * from combined_filings
