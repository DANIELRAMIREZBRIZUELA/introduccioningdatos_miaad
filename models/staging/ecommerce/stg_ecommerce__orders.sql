select
    order_id,
    cast(created_at as timestamp) as order_created_at,
    website_session_id,
    user_id,
    primary_product_id,
    items_purchased,
    price_usd,
    cogs_usd,
    (price_usd - cogs_usd) as margin_usd
from {{ source('ecommerce_raw', 'orders') }}
