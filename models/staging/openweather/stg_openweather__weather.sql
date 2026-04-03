with source as (
    select
        lat,
        lon,
        timezone,
        timezone_offset,
        daily,
        _airbyte_raw_id,
        _airbyte_extracted_at
    from {{ source('openweather_raw', 'raw_weather') }}
),

daily_exploded as (
    select
        s.lat,
        s.lon,
        s.timezone,
        s.timezone_offset,
        s._airbyte_raw_id,
        s._airbyte_extracted_at,
        d.value as daily_item
    from source as s,
        json_each(s.daily) as d
    where s.daily is not null
)

select
    _airbyte_raw_id,
    _airbyte_extracted_at,
    lat,
    lon,
    coalesce(replace(split_part(timezone, '/', 2), '_', ' '), 'Unknown City') as city_name,
    'N/A' as country_code,
    cast(json_extract_string(daily_item, '$.weather[0].main') as varchar) as weather_main,
    cast(json_extract_string(daily_item, '$.weather[0].description') as varchar) as weather_description,
    cast(json_extract(daily_item, '$.dt') as bigint) as observation_epoch,
    cast(to_timestamp(cast(json_extract(daily_item, '$.dt') as bigint)) as timestamp) as observation_ts,
    cast(date_trunc('day', to_timestamp(cast(json_extract(daily_item, '$.dt') as bigint))) as date) as observation_date,
    cast(json_extract(daily_item, '$.temp.day') as double) as temperature_c,
    cast(json_extract(daily_item, '$.feels_like.day') as double) as feels_like_c,
    cast(json_extract(daily_item, '$.temp.min') as double) as min_temp_c,
    cast(json_extract(daily_item, '$.temp.max') as double) as max_temp_c,
    cast(json_extract(daily_item, '$.pressure') as integer) as pressure_hpa,
    cast(json_extract(daily_item, '$.humidity') as integer) as humidity_pct,
    cast(json_extract(daily_item, '$.wind_speed') as double) as wind_speed_ms,
    cast(json_extract(daily_item, '$.wind_deg') as integer) as wind_direction_deg,
    cast(json_extract(daily_item, '$.clouds') as integer) as cloudiness_pct,
    cast(json_extract(daily_item, '$.sunrise') as bigint) as sunrise_epoch,
    cast(json_extract(daily_item, '$.sunset') as bigint) as sunset_epoch,
    current_timestamp as dbt_loaded_at
from daily_exploded
where json_extract(daily_item, '$.dt') is not null
