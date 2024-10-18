with company_info as (
    select
        id,
        ticker,
        request_timestamp,
        company_name,
        sector,
        industry,
        country,
        current_price,
        market_cap,
        shares_outstanding,
        earnings_per_share,
        price_earnings_ratio
    from {{ ref('stg_yahoo_company_infos') }}
)

select * from company_info
