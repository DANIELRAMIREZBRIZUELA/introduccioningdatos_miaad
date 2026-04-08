select
    website_pageview_id,
    cast(created_at as timestamp) as pageview_created_at,
    website_session_id,
    pageview_url
from {{ source('ecommerce_raw', 'website_pageviews') }}
