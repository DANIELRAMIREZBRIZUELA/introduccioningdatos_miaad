select
    o.order_id,
    o.order_created_at,
    o.order_date,
    o.website_session_id,
    s.user_id,
    s.device_type,
    s.utm_source,
    s.utm_campaign,
    s.http_referer,
    o.primary_product_id,
    o.primary_product_name,
    o.total_items,
    o.order_revenue_usd,
    o.order_cogs_usd,
    o.order_margin_usd,
    o.refunds_usd,
    o.net_revenue_usd,
    o.net_margin_usd
from {{ ref('int_ecommerce__orders_enriched') }} o
left join {{ ref('stg_ecommerce__sessions') }} s
    on o.website_session_id = s.website_session_id
