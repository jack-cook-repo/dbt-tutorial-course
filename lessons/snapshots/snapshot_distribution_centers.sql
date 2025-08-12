{% snapshot snapshot_distribution_center%}
{{
    config(
      target_schema='dbt_test',
      unique_key='id',
      strategy='check',
      check_cols=['name', 'latitude', 'longitude']
    )
}}
select * from {{ source('dbt_arihant', 'seed_distribution_centers') }}
{% endsnapshot %}