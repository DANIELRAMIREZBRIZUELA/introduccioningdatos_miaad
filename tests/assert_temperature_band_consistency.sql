select
  city_name,
  observation_date,
  avg_temperature_c,
  temperature_band
from {{ ref('fct_openweather_daily_weather') }}
where (avg_temperature_c < 10 and temperature_band != 'cold')
   or (avg_temperature_c >= 10 and avg_temperature_c < 25 and temperature_band != 'mild')
   or (avg_temperature_c >= 25 and temperature_band != 'warm')
