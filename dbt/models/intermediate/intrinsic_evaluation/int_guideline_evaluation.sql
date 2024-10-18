with moat as (
    select
        filing_id,
        ticker,
        country,
        sector,
        moat_score
    from {{ ref('int_moat_evaluation') }}
),

financial_health as (
    select
        filing_id,
        financial_health_score
    from {{ ref('int_financial_health_evaluation') }}
),

efficiency as (
    select
        filing_id,
        efficiency_score
    from {{ ref('int_efficiency_evaluation') }}
),

management as (
    select
        filing_id,
        management_score
    from {{ ref('int_management_evaluation') }}
)

select
    m.filing_id,
    m.ticker,
    m.country,
    m.sector,
    m.moat_score,
    f.financial_health_score,
    e.efficiency_score,
    mg.management_score,
    coalesce(m.moat_score, 0)
    + coalesce(f.financial_health_score, 0)
    + coalesce(e.efficiency_score, 0)
    + coalesce(mg.management_score, 0) as total_score
from moat as m
left join financial_health as f on m.filing_id = f.filing_id
left join efficiency as e on m.filing_id = e.filing_id
left join management as mg on m.filing_id = mg.filing_id
