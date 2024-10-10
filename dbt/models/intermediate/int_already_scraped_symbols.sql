-- use balance sheets since profiles and company infos should get updated regularly to fetch the current price more frequently.
with all_already_scraped_tickers as (
    select
        ticker,
        end_of_period
    from {{ ref('stg_fmp_balance_sheets') }}
    union all
    select
        ticker,
        end_of_period
    from {{ ref('stg_yahoo_balance_sheets_yearly') }}
),

unique_already_scraped_tickers as (
    select distinct ticker from all_already_scraped_tickers
    where end_of_period > date_sub(current_date(), interval 1 year)
)

select * from unique_already_scraped_tickers
