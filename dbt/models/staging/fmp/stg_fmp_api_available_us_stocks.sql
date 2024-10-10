select symbol as ticker
from {{ ref('seed_fmp_available_stocks') }}
where price > 1 and type = "stock" and exchange in (
        "NASDAQ", "New York Stock Exchange", "NASDAQ Capital Market", "NASDAQ Global Market", "NASDAQ Global Select"
    )
