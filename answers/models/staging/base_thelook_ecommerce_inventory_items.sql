with source as (
      select * from {{ source('thelook_ecommerce', 'inventory_items') }}
),
renamed as (
    select
        {{ adapter.quote("id") }},
        {{ adapter.quote("product_id") }},
        {{ adapter.quote("created_at") }},
        {{ adapter.quote("sold_at") }},
        {{ adapter.quote("cost") }},
        {{ adapter.quote("product_category") }},
        {{ adapter.quote("product_name") }},
        {{ adapter.quote("product_brand") }},
        {{ adapter.quote("product_retail_price") }},
        {{ adapter.quote("product_department") }},
        {{ adapter.quote("product_sku") }},
        {{ adapter.quote("product_distribution_center_id") }}

    from source
)
select * from renamed
  