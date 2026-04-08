select
    order_item_id,
    cast(created_at as timestamp) as order_item_created_at,
    order_id,
    product_id,
    is_primary_item,
    price_usd,
    cogs_usd,
    (price_usd - cogs_usd) as item_margin_usd
from {{ source('ecommerce_raw', 'order_items') }}
