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
        date(calendaryear, 12, 31) as end_of_period
    from {{ source('financial_modeling_prep', 'balance_sheet') }}
)

select *
from source_data
