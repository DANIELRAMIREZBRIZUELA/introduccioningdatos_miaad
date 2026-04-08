with orders as (
    select * from {{ ref('stg_ecommerce__orders') }}
),
order_items as (
    select * from {{ ref('stg_ecommerce__order_items') }}
),
products as (
    select * from {{ ref('stg_ecommerce__products') }}
),
refunds_by_order as (
    select
        order_id,
        sum(refund_amount_usd) as total_refunds_usd
    from {{ ref('stg_ecommerce__refunds') }}
    group by 1
),
items_by_order as (
    select
        oi.order_id,
        sum(oi.price_usd) as gross_item_revenue_usd,
        sum(oi.item_margin_usd) as gross_item_margin_usd,
        count(*) as total_items
    from order_items oi
    group by 1
),
primary_product as (
    select
        oi.order_id,
        p.product_name as primary_product_name
    from order_items oi
    left join products p
        on oi.product_id = p.product_id
    where oi.is_primary_item = 1
)
select
    o.order_id,
    o.order_created_at,
    cast(date_trunc('day', o.order_created_at) as date) as order_date,
    o.website_session_id,
    o.user_id,
    o.primary_product_id,
    pp.primary_product_name,
    coalesce(ibo.total_items, o.items_purchased) as total_items,
    o.price_usd as order_revenue_usd,
    o.cogs_usd as order_cogs_usd,
    o.margin_usd as order_margin_usd,
    coalesce(rbo.total_refunds_usd, 0) as refunds_usd,
    o.price_usd - coalesce(rbo.total_refunds_usd, 0) as net_revenue_usd,
    o.margin_usd - coalesce(rbo.total_refunds_usd, 0) as net_margin_usd
from orders o
left join items_by_order ibo
    on o.order_id = ibo.order_id
left join refunds_by_order rbo
    on o.order_id = rbo.order_id
left join primary_product pp
    on o.order_id = pp.order_id
