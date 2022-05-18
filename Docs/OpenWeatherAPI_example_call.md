# OpenWeatherAPI Example Call

1. Before you can query ‘points(ViewPoint)’ you must subscribe to a data set

```graphql
mutation {
  set_channel(channel: 1, data_set: "openweather_temp") {
    name
    display_type
    color_set
    min_val
    max_val
    error
  }
}
```

1. You may now make a query ‘points(ViewPoint)’

```graphql
query {
  points(viewport: { lat1: 40.2, lon1: -93.2, lat2: 43.5, lon2: -92.5, interval: 1.0 }, channel: 1) {
  	lat
    lon
    value1
  }
}
```

1. Result

```graphql
{
  "data": {
    "points": [
        {
          "lat": 40.2,
          "lon": -93.2,
          "value": 41.07
        },
        {
          "lat": 40.2,
          "lon": -92.2,
          "value": 39.42
        },
        {
          "lat": 41.2,
          "lon": -93.2,
          "value": 38.01
        },
        {
          "lat": 41.2,
          "lon": -92.2,
          "value": 37.02
        },
        {
          "lat": 42.2,
          "lon": -93.2,
          "value": 35.13
        },
        {
          "lat": 42.2,
          "lon": -92.2,
          "value": 32.79
        },
        {
          "lat": 43.2,
          "lon": -93.2,
          "value": 31.77
        },
        {
          "lat": 43.2,
          "lon": -92.2,
          "value": 28.08
        },
        {
          "lat": 44.2,
          "lon": -93.2,
          "value": 30.6
        },
        {
          "lat": 44.2,
          "lon": -92.2,
          "value": 28
        }
    ]
  }
}
```