resource "google_bigquery_table" "financial_ratios" {
  dataset_id          = google_bigquery_dataset.curated_dataset.dataset_id
  table_id            = "financial_ratios_over_time"
  project             = var.project_id
  deletion_protection = false # This table can always be re-generated from raw data
  schema              = <<EOF
[
    {
        "name": "id",
        "type": "STRING",
        "mode": "REQUIRED"
    },
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
        "name": "end_of_period",
        "type": "DATE",
        "mode": "REQUIRED"
    },
    {
        "name": "free_cash_flow_over_revenue",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "net_margin_over_revenue",
        "type": "FLOAT",
        "mode": "NULLABLE"
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
        "type": "INTEGER",
        "mode": "REQUIRED"
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
        "name": "filing_id",
        "type": "STRING",
        "mode": "NULLABLE"
    },
    {
        "name": "total_revenue",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "net_income",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "cost_of_goods_sold",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "selling_general_and_administration",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "free_cash_flow",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "dividends_paid",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "stockholders_equity",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "total_assets",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "accounts_receivable",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "cash_and_cash_equivalents",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "current_assets",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "current_liabilities",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "inventory",
        "type": "FLOAT",
        "mode": "NULLABLE"
    },
    {
        "name": "long_term_debt",
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
    }
] 
EOF
}
