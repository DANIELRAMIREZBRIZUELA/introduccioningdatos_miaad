with summary as (
    select *
    from {{ ref('int_openweather__daily_summary') }}
)

select
    city_name,
    country_code,
    observation_date,
    observation_count,
    avg_temperature_c,
    min_temperature_c,
    max_temperature_c,
    avg_feels_like_c,
    avg_humidity_pct,
    avg_pressure_hpa,
    avg_wind_speed_ms,
    avg_cloudiness_pct,
    case
        when avg_cloudiness_pct >= 75 then 'very_cloudy'
        when avg_cloudiness_pct >= 40 then 'partly_cloudy'
        else 'clear'
    end as sky_condition,
    case
        when avg_temperature_c < 10 then 'cold'
        when avg_temperature_c < 25 then 'mild'
        else 'warm'
    end as temperature_band
from summary
