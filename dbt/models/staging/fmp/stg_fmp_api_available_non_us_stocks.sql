select symbol as ticker
from {{ ref('seed_fmp_available_stocks') }}
where price > 1 and type = "stock" and exchange in (
        "London Stock Exchange",
        "Tokyo",
        "Frankfurt Stock Exchange",
        "Toronto Stock Exchange",
        "Paris",
        "Toronto Stock Exchange Ventures",
        "Stockholm Stock Exchange",
        "Canadian Securities Exchange",
        "Swiss Exchange",
        "Copenhagen",
        "Milan",
        "Nasdaq",
        "Warsaw Stock Exchange",
        "Amsterdam",
        "Oslo Stock Exchange",
        "Brussels",
        "Helsinki",
        "Madrid Stock Exchange",
        "Stuttgart"
    )
