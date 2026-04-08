with sessions as (
    select
        cast(date_trunc('day', session_created_at) as date) as session_date,
        count(*) as total_sessions
    from {{ ref('stg_ecommerce__sessions') }}
    group by 1
),
orders as (
    select
        order_date,
        count(*) as total_orders,
        sum(net_revenue_usd) as net_revenue_usd,
        sum(net_margin_usd) as net_margin_usd
    from {{ ref('int_ecommerce__orders_enriched') }}
    group by 1
)
select
    s.session_date,
    s.total_sessions,
    coalesce(o.total_orders, 0) as total_orders,
    coalesce(o.net_revenue_usd, 0) as net_revenue_usd,
    coalesce(o.net_margin_usd, 0) as net_margin_usd,
    case
        when s.total_sessions = 0 then 0
        else round((coalesce(o.total_orders, 0) * 100.0) / s.total_sessions, 2)
    end as conversion_rate_pct,
    case
        when coalesce(o.total_orders, 0) = 0 then 0
        else round(coalesce(o.net_revenue_usd, 0) / o.total_orders, 2)
    end as aov_usd
from sessions s
left join orders o
    on s.session_date = o.order_date
