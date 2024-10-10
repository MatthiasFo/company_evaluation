with source_data as (
    select
        id,
        ticker,
        shortname as company_name,
        sector,
        industry,
        currentprice as current_price,
        marketcap as market_cap,
        sharesoutstanding as shares_outstanding,
        request_timestamp,
        case when country = "US" then "United States" else country end as country,
        coalesce(trailingeps, forwardeps) as earnings_per_share,
        coalesce(trailingpe, forwardpe) as price_earnings_ratio
        -- available on some yahoo data but these figures are calculated with the base data anyway
        -- revenuegrowth as revenue_growth,
        -- currentratio as current_ratio,
        -- quickratio as quick_ratio,
        -- grossmargins as gross_margins,
        -- operatingmargins as operating_margins,
        -- returnonassets as return_on_assets,
        -- returnonequity as return_on_equity,
        -- enterprisevalue as enterprise_value,
    from {{ source('yahoo_finance', 'company_info') }}
)

select *
from source_data
