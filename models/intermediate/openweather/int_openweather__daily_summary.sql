with weather as (
    select *
    from {{ ref('stg_openweather__weather') }}
),

summary as (
    select
        city_name,
        country_code,
        observation_date,
        count(*) as observation_count,
        avg(temperature_c) as avg_temperature_c,
        min(temperature_c) as min_temperature_c,
        max(temperature_c) as max_temperature_c,
        avg(feels_like_c) as avg_feels_like_c,
        avg(humidity_pct) as avg_humidity_pct,
        avg(pressure_hpa) as avg_pressure_hpa,
        avg(wind_speed_ms) as avg_wind_speed_ms,
        avg(cloudiness_pct) as avg_cloudiness_pct
    from weather
    group by 1, 2, 3
)

select *
from summary
