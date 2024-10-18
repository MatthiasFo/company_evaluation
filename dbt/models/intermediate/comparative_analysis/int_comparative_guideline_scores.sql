with guideline_scores as (
    select
        ticker,
        max(country) as country,
        max(sector) as sector,
        avg(moat_score) as avg_moat_score,
        avg(financial_health_score) as avg_financial_health_score,
        avg(efficiency_score) as avg_efficiency_score,
        avg(management_score) as avg_management_score,
        avg(total_score) as avg_total_score
    from {{ ref('int_guideline_evaluation') }}
    group by ticker
),

averages as (
    select
        sector,
        country,
        avg(moat_score) as comp_moat_score,
        avg(financial_health_score) as comp_financial_health_score,
        avg(efficiency_score) as comp_efficiency_score,
        avg(management_score) as comp_management_score,
        avg(total_score) as comp_total_score
    from {{ ref('int_guideline_evaluation') }}
    group by sector, country
),

final_scores as (
    select
        ticker,
        avg_moat_score,
        a.comp_moat_score,
        avg_financial_health_score,
        a.comp_financial_health_score,
        avg_efficiency_score,
        a.comp_efficiency_score,
        avg_management_score,
        a.comp_management_score,
        avg_total_score,
        a.comp_total_score,
        (
            case
                when avg_moat_score > a.comp_moat_score then 1 else 0
            end
            + case
                when avg_financial_health_score > a.comp_financial_health_score then 1 else 0
            end
            + case
                when avg_efficiency_score > a.comp_efficiency_score then 1 else 0
            end
            + case
                when avg_management_score > a.comp_management_score then 1 else 0
            end
            + case
                when avg_total_score > a.comp_total_score then 1 else 0
            end
        ) as final_score
    from guideline_scores as g
    inner join averages as a on g.sector = a.sector and g.country = a.country
)

select * from final_scores
