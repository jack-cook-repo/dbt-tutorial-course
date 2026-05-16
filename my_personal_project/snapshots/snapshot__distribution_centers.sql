{% snapshot snapshot__distribution_centers %}

{{
	config(
		target_schema='dbt_snapshots',
		strategy='check',
		unique_key='id',
		check_cols=['name', 'latitude', 'longitude']
	)
}}
-- Selecciona las columnas necesarias; usa ref() o source() según tu proyecto
select
	id,
	name,
	latitude,
	longitude
from {{ ref('stg_ecommerce__distribution_centers') }}
{% endsnapshot %}