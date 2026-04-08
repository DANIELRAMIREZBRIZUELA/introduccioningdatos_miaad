select
    product_id,
    cast(created_at as timestamp) as product_created_at,
    product_name
from {{ source('ecommerce_raw', 'products') }}
