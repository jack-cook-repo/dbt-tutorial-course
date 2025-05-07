{% snapshot snapshot_distribution_centers %}
{{
    config(
        target_database = "bigquery-public-data",
        target_schema = 'dbt_snapshot',
        unique_key = 'id',
        strategy = 'check',
        check_cols = 'all'
    )
}}

SELECT * from {{ source('thelook_ecommerce','distribution_centers') }}

{% endsnapshot %}
