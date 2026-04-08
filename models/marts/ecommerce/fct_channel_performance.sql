with sessions as (
    select
        coalesce(utm_source, 'direct') as utm_source,
        coalesce(utm_campaign, 'none') as utm_campaign,
        count(*) as total_sessions
    from {{ ref('stg_ecommerce__sessions') }}
    group by 1, 2
),
orders as (
    select
        coalesce(s.utm_source, 'direct') as utm_source,
        coalesce(s.utm_campaign, 'none') as utm_campaign,
        count(distinct o.order_id) as total_orders,
        sum(o.net_revenue_usd) as net_revenue_usd,
        sum(o.net_margin_usd) as net_margin_usd
    from {{ ref('int_ecommerce__orders_enriched') }} o
    left join {{ ref('stg_ecommerce__sessions') }} s
        on o.website_session_id = s.website_session_id
    group by 1, 2
)
select
    s.utm_source,
    s.utm_campaign,
    s.total_sessions,
    coalesce(o.total_orders, 0) as total_orders,
    coalesce(o.net_revenue_usd, 0) as net_revenue_usd,
    coalesce(o.net_margin_usd, 0) as net_margin_usd,
    case
        when s.total_sessions = 0 then 0
        else round((coalesce(o.total_orders, 0) * 100.0) / s.total_sessions, 2)
    end as conversion_rate_pct,
    case
        when s.total_sessions = 0 then 0
        else round(coalesce(o.net_revenue_usd, 0) / s.total_sessions, 2)
    end as revenue_per_session_usd
from sessions s
left join orders o
    on s.utm_source = o.utm_source
   and s.utm_campaign = o.utm_campaign
