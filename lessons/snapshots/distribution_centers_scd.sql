{%{% snapshot distribution_centers_scd %}
{{
   config(
       target_schema='dbt_ep',
       unique_key='id',
       strategy='check',
       check_cols=["name",'latitude','longitude']
   )
}}

SELECT  id,
        name,
        latitude,
        longitude
FROM {{ ref('seed_distribution_centers_new') }}

{% endsnapshot %}%}