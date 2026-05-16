WITH distribution_centers AS (
	SELECT *

	FROM {{ source('thelook_ecommerce', 'distribution_centers') }}
),
seed_distribution_centers AS (
	SELECT *
	FROM {{ ref('seed_distribution_centers_added') }}
)

SELECT
	id,
	name,
	latitude,
	longitude,
	distribution_center_geom
FROM distribution_centers
union all
SELECT
	id,
	name,
	latitude,
	longitude,
	null distribution_center_geom
FROM seed_distribution_centers
ORDER BY id