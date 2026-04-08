select
    order_item_refund_id,
    cast(created_at as timestamp) as refund_created_at,
    order_item_id,
    order_id,
    refund_amount_usd
from {{ source('ecommerce_raw', 'order_item_refunds') }}
