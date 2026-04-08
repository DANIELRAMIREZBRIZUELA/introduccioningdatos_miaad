-- Suggested query 1: Daily sessions and orders
SELECT
  session_date,
  total_sessions,
  total_orders,
  gross_revenue_usd,
  conversion_rate_pct,
  aov_usd
FROM main.fct_daily_sales
ORDER BY session_date;

-- Suggested query 2: Channel performance ranking
SELECT
  coalesce(utm_source, '(none)') as utm_source,
  coalesce(utm_campaign, '(none)') as utm_campaign,
  total_sessions,
  total_orders,
  gross_revenue_usd,
  revenue_per_session_usd,
  conversion_rate_pct
FROM main.fct_channel_performance
ORDER BY gross_revenue_usd DESC;

-- Suggested query 3: Refund share by product
SELECT
  primary_product_name,
  count(*) as orders,
  sum(CASE WHEN refunds_usd > 0 THEN 1 ELSE 0 END) as refunded_orders,
  100.0 * sum(CASE WHEN refunds_usd > 0 THEN 1 ELSE 0 END) / count(*) as refund_rate_pct
FROM main.obt_orders_enriched
GROUP BY 1
ORDER BY refund_rate_pct DESC;

-- Suggested query 4: Device split
SELECT
  device_type,
  count(*) as orders,
  sum(net_revenue_usd) as net_revenue_usd,
  avg(net_revenue_usd) as avg_order_net_revenue_usd
FROM main.obt_orders_enriched
GROUP BY 1
ORDER BY net_revenue_usd DESC;

-- Suggested query 5: Monthly trend
SELECT
  date_trunc('month', session_date) as month,
  sum(total_sessions) as total_sessions,
  sum(total_orders) as total_orders,
  sum(gross_revenue_usd) as gross_revenue_usd
FROM main.fct_daily_sales
GROUP BY 1
ORDER BY month;
