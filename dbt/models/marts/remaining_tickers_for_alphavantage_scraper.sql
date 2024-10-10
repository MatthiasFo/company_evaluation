select ticker
-- alphavantage has a strong limit on API calls in the free version therefore
-- 1. it is only used to fill historic balance sheet, income statement and cash flow data 
--    as it is the only API providing data more than 5 years back
--    -> no profile calls or others. these are done with yahoo and FMP
-- 2. it is first used to fill US historic stock data
from {{ ref('stg_fmp_api_available_us_stocks') }}
where ticker in (select ticker from {{ ref('int_already_scraped_symbols') }})
