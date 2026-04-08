select
    website_session_id,
    cast(created_at as timestamp) as session_created_at,
    user_id,
    is_repeat_session,
    utm_source,
    utm_campaign,
    utm_content,
    device_type,
    http_referer
from {{ source('ecommerce_raw', 'website_sessions') }}
