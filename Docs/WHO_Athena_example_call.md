# WHO Athena Example Call

1. Before you can query ‘points(ViewPoint)’ you must subscribe to a data set

```graphql
mutation {
  set_channel(channel: 0, data_set: "Life expectancy at birth (years)") {
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
  points(viewport: { lat1: 40.2, lon1: -93.2, lat2: 43.5, lon2: -92.5, interval: 1.0 }, channel: 0) {
  	lat
    lon
    value1
		value2
  }
}
```

1. Result

```graphql
{
  "data": {
    "points": [
       {
        "lat": 44,
        "lon": 2,
        "value1": 52,
        "value2": null
      },
      {
        "lat": 45,
        "lon": 2,
        "value1": 52,
        "value2": null
      },
      {
        "lat": 99,
        "lon": 2,
        "value1": 69.3,
        "value2": null
      },
      {
        "lat": 100,
        "lon": 2,
        "value1": 69.3,
        "value2": null
      },
      {
        "lat": 101,
        "lon": 2,
        "value1": 69.3,
        "value2": null
      },
			.
			.
			.
    ]
  }
}
```