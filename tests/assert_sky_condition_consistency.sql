select
  city_name,
  observation_date,
  avg_cloudiness_pct,
  sky_condition
from {{ ref('fct_openweather_daily_weather') }}
where (avg_cloudiness_pct >= 75 and sky_condition != 'very_cloudy')
   or (avg_cloudiness_pct >= 40 and avg_cloudiness_pct < 75 and sky_condition != 'partly_cloudy')
   or (avg_cloudiness_pct < 40 and sky_condition != 'clear')
