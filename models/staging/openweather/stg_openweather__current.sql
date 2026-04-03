with source as (
    select
        _airbyte_raw_id,
        _airbyte_extracted_at,
        lat,
        lon,
        timezone,
        timezone_offset,
        current
    from {{ source('openweather_raw', 'raw_weather_current') }}
)

select
    _airbyte_raw_id,
    _airbyte_extracted_at,
    lat,
    lon,
    coalesce(replace(split_part(timezone, '/', 2), '_', ' '), 'Unknown City') as city_name,
    'N/A' as country_code,
    cast(json_extract_string(current, '$.weather[0].main') as varchar) as weather_main,
    cast(json_extract_string(current, '$.weather[0].description') as varchar) as weather_description,
    cast(json_extract(current, '$.dt') as bigint) as observation_epoch,
    cast(to_timestamp(cast(json_extract(current, '$.dt') as bigint)) as timestamp) as observation_ts,
    cast(date_trunc('day', to_timestamp(cast(json_extract(current, '$.dt') as bigint))) as date) as observation_date,
    cast(json_extract(current, '$.temp') as double) as temperature_c,
    cast(json_extract(current, '$.feels_like') as double) as feels_like_c,
    cast(json_extract(current, '$.pressure') as integer) as pressure_hpa,
    cast(json_extract(current, '$.humidity') as integer) as humidity_pct,
    cast(json_extract(current, '$.wind_speed') as double) as wind_speed_ms,
    cast(json_extract(current, '$.wind_deg') as integer) as wind_direction_deg,
    cast(json_extract(current, '$.clouds') as integer) as cloudiness_pct,
    cast(json_extract(current, '$.sunrise') as bigint) as sunrise_epoch,
    cast(json_extract(current, '$.sunset') as bigint) as sunset_epoch,
    current_timestamp as dbt_loaded_at
from source
where current is not null
  and json_extract(current, '$.dt') is not null
