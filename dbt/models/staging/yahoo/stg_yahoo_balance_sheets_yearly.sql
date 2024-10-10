with source_data as (
    select
        id,
        ticker,
        country,
        industry,
        end_of_period,
        stockholders_equity,
        total_assets,
        accounts_receivable,
        allowance_for_doubtful_accounts_receivable,
        cash_and_cash_equivalents,
        current_assets,
        current_liabilities,
        inventory,
        -- necessary to calculate growth in shares. also close to outstanding shares is share_issued
        ordinary_shares_number as outstanding_shares,
        coalesce(long_term_debt, long_term_debt_and_capital_lease_obligation) as long_term_debt
    from {{ source('yahoo_finance', 'balance_sheet_yearly') }}
)

select *
from source_data
