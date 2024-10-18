with base as (
    select
        ticker,
        max(sector) as sector,
        max(country) as country,
        avg(price_earnings_ratio) as avg_price_earnings_ratio,
        avg(price_to_sales_ratio) as avg_price_to_sales_ratio,
        avg(price_to_book_ratio) as avg_price_to_book_ratio,
        avg(price_to_dcf_normal_evaluation) as avg_price_to_dcf_normal_evaluation,
        avg(earnings_yield) as avg_earnings_yield,
        avg(cash_return) as avg_cash_return
    from {{ ref('int_multiple_valuations') }}
    group by ticker
),

competition as (
    select
        sector,
        country,
        avg(price_earnings_ratio) as comp_price_earnings_ratio,
        avg(price_to_sales_ratio) as comp_price_to_sales_ratio,
        avg(price_to_book_ratio) as comp_price_to_book_ratio,
        avg(price_to_dcf_normal_evaluation) as comp_price_to_dcf_normal_evaluation,
        avg(earnings_yield) as comp_earnings_yield,
        avg(cash_return) as comp_cash_return
    from {{ ref('int_multiple_valuations') }}
    group by sector, country
),

final_scores as (
    select
        b.ticker,
        b.sector,
        b.country,
        b.avg_price_earnings_ratio,
        b.avg_price_to_sales_ratio,
        b.avg_price_to_book_ratio,
        b.avg_price_to_dcf_normal_evaluation,
        b.avg_earnings_yield,
        b.avg_cash_return,
        c.comp_price_earnings_ratio,
        c.comp_price_to_sales_ratio,
        c.comp_price_to_book_ratio,
        c.comp_price_to_dcf_normal_evaluation,
        c.comp_earnings_yield,
        c.comp_cash_return,
        -- Calculate the final score based on the comparison
        (
            case
                when b.avg_price_earnings_ratio < c.comp_price_earnings_ratio then 1 else 0
            end
            + case
                when b.avg_price_to_sales_ratio < c.comp_price_to_sales_ratio then 1 else 0
            end
            + case
                when b.avg_price_to_book_ratio < c.comp_price_to_book_ratio then 1 else 0
            end
            + case
                when b.avg_price_to_dcf_normal_evaluation < c.comp_price_to_dcf_normal_evaluation then 1 else 0
            end
            + case
                when b.avg_earnings_yield > c.comp_earnings_yield then 1 else 0
            end
            + case
                when b.avg_cash_return > c.comp_cash_return then 1 else 0
            end
        ) as final_score
    from base as b
    inner join competition as c on b.sector = c.sector and b.country = c.country
)

select * from final_scores
