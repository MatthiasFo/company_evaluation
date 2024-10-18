with fmp_infos_with_row_count as (
    select
        *,
        row_number() over (partition by ticker order by request_timestamp desc) as rn_latest
    from {{ ref('int_fmp_company_infos') }}
),

yahoo_infos_with_row_count as (
    select
        *,
        row_number() over (partition by ticker order by request_timestamp desc) as rn_latest
    from {{ ref('int_yahoo_company_infos') }}
),

latest_company_infos as (
    select *
    from fmp_infos_with_row_count
    where rn_latest = 1
    union all
    select *
    from yahoo_infos_with_row_count
    where rn_latest = 1
),

latest_with_row_num_for_deduplication as (
    select
        *,
        row_number() over (partition by ticker order by request_timestamp desc) as rn_dedupl
    from latest_company_infos
)

select
    id,
    ticker,
    request_timestamp,
    company_name,
    industry,
    sector,
    current_price,
    market_cap,
    shares_outstanding,
    earnings_per_share,
    price_earnings_ratio,
    country
from latest_with_row_num_for_deduplication
where rn_dedupl = 1
    and shares_outstanding > 0 -- companies without shares outstanding are not useful
    and market_cap > 0 -- market cap is necessary for enterprise value calculation
    and current_price > 0 -- companies without current price are not useful
    and company_name is not null -- need company name to identify the company
