select ticker
-- on the free version of the FMP API you only get US stocks
from {{ ref('stg_fmp_api_available_us_stocks') }}
where ticker not in (select ticker from {{ ref('int_already_scraped_symbols') }})
