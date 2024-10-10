resource "google_bigquery_table" "intrinsic_value_and_ratio_evaluations" {
  dataset_id          = google_bigquery_dataset.curated_dataset.dataset_id
  table_id            = "intrinsic_value_and_ratio_evaluations"
  project             = var.project_id
  deletion_protection = false # This table can always be re-generated from raw data
  schema              = <<EOF
[
    {
        "name": "ticker",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "company_name",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "country",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "industry",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "sector",
        "type": "STRING",
        "mode": "REQUIRED"
    },
    {
        "name": "free_cash_flow_over_revenue",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "net_margin_over_revenue",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "return_on_assets",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "return_on_equity",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "asset_turnover_ratio",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory_turnover_ratio",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory_over_revenue",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "sga_over_revenue",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "current_ratio",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "quick_ratio",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "fin_leverage",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "accounts_receivable_over_revenue",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "earnings_yield",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "cash_return",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "guideline_score",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "free_cash_flow_over_revenue_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "net_margin_over_revenue_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "return_on_assets_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "return_on_equity_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "asset_turnover_ratio_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory_turnover_ratio_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory_over_revenue_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "sga_over_revenue_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "current_ratio_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "quick_ratio_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "fin_leverage_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "accounts_receivable_over_revenue_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "earnings_yield_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "cash_return_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "revenue_growth",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "shares_growth",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "sga_over_revenue_change",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory_over_revenue_change",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "accounts_receivable_over_revenue_change",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "sga_over_revenue_change_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory_over_revenue_change_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "accounts_receivable_over_revenue_change_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "shares_growth_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "current_price",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "normal",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "stable",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "stable_and_strong_growth",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "volatile",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "volatile_and_weak_growth",
        "type": "FLOAT",
        "mode": "REQUIRED"
    },
    {
        "name": "current_price_over_normal_dcf",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "free_cash_flow",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "shares_outstanding",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "guideline_score_competition",
        "type": "FLOAT",
        "mode": "NULLABLE"
    }
]
EOF
}