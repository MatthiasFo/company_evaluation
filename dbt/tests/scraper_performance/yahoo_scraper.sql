{{ config(severity = 'warn') }}

with tickers_scraped_last_week as (
    select
        ticker,
        datetime_trunc(request_timestamp, day) as request_day
    from {{ ref('stg_yahoo_company_infos') }}
    where request_timestamp >= datetime_sub(current_date(), interval 1 week) and request_timestamp < current_date()
),

-- use date array to catch days where scraper did not fetch any data at all
date_array as (
    select dt
    -- TODO: Extend this to 1 week as soon as the scraper is running stable for a week
    from unnest(generate_date_array(date_sub(current_date(), interval 1 day), current_date(), interval 1 day)) as dt
    where dt < current_date() -- exclude today because we do not have the full data yet
),

count_per_day as (
    select
        request_day,
        count(distinct ticker) as num_tickers
    from tickers_scraped_last_week group by request_day
),

last_week as (
    select
        da.dt,
        cpd.num_tickers
    from date_array as da left join count_per_day as cpd on da.dt = cpd.request_day
)

select *
from last_week
where num_tickers < 350 or num_tickers is null
