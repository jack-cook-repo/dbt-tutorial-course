{% snapshot snapshots_orders %}

{{ config(
    target_schema='dbt_snapshots',
    unique_key='order_id',
    strategy='check',
    check_cols=['order_id', 'user_id', 'status']
)}}

select * from {{ ref('stg_ecommerce_orders')}}

{% endsnapshot  %}