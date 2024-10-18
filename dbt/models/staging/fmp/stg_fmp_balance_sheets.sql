with source_data as (
    select
        id,
        symbol as ticker,
        totalstockholdersequity as stockholders_equity,
        totalassets as total_assets,
        netreceivables as accounts_receivable,
        cashandcashequivalents as cash_and_cash_equivalents,
        totalcurrentassets as current_assets,
        totalcurrentliabilities as current_liabilities,
        inventory,
        longtermdebt as long_term_debt,
        /* The number of common stock typically refers to the authorized shares,
        which is the maximum number of shares a company is legally allowed to issue,
        as approved by its shareholders or governing body.
        The number of outstanding shares represents the total number of shares that have been issued and are currently held by shareholders,
        including both institutional investors and individual shareholders. */
        commonstock as outstanding_shares,
        date(calendaryear, 12, 31) as end_of_period
    from {{ source('financial_modeling_prep', 'balance_sheet') }}
)

select *
from source_data
