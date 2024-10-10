with source_data as (
    select
        id,
        symbol as ticker,
        totalshareholderequity as stockholders_equity,
        totalassets as total_assets,
        currentnetreceivables as accounts_receivable,
        cashandcashequivalentsatcarryingvalue as cash_and_cash_equivalents,
        totalcurrentassets as current_assets,
        currentdebt as current_liabilities,
        inventory,
        longtermdebt as long_term_debt,
        commonStockSharesOutstanding as outstanding_shares,
        fiscaldateending as end_of_period
    from {{ source('alphavantage', 'balance_sheets_annually') }}
)

select * from source_data
