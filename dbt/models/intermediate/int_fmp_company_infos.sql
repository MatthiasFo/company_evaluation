with company_info as (
    select
        profiles.id,
        profiles.ticker,
        profiles.request_timestamp,
        profiles.company_name,
        profiles.sector,
        profiles.industry,
        profiles.country,
        profiles.current_price,
        profiles.market_cap,
        quotes.shares_outstanding,
        quotes.earnings_per_share,
        quotes.price_earnings_ratio
    from {{ ref('stg_fmp_profiles') }} as profiles
    inner join {{ref('stg_fmp_quotes')}} as quotes on profiles.id = quotes.id
)

select * from company_info
