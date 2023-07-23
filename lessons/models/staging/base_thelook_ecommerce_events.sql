with source as (
      select * from {{ source('thelook_ecommerce', 'events') }}
),
renamed as (
    select
        

    from source
)
select * from renamed
  