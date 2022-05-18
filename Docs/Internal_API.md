# Internal API

## Data Types

```graphql
# The following section describes the custom data types made
# by the team to create a GraphQL API

# ! == Required

# Value(s) at each lon/lat coordinate
# This is the result data type that is sent to the front end 
# when a query is made for data 
type DataPoint {
  lon: Float!
  lat: Float!
  value1: Float!
	value2: Float
}

# Description of subscribed DataSet (ie. openweather_humidity)
type DataSet {
  name: String
  display_type: String
  color_set: String
  min_val: Float
  max_val: Float
  error: String
}

# Coordinate range / interval input parameter 
input Viewport {
  lat1: Float!
  lon1: Float!
  lat2: Float!
  lon2: Float!
  interval: Float!
}
```

## Queries

```graphql
# Input: Viewport, channel, year (WHO data input)
# Result: returns an array of DataPoint's    
points(viewport: Viewport!, channel: Int!, year: String): [DataPoint!]

# Result: String array of subscribed channels according to channel number
channels(): [String]!

# Result: String array of all available data sets to subscribe to
datasets(): [String]!
```

## Mutations

```graphql
# Input: channel number (0 - 3) | data_set: chosen data set (ie. openweather_temp)
# Result: Returns description of subscribed data set 
set_channel(channel: Int! data_set: String!): DataSet!

# Input: channel number (0-3)
# Result: True if channel was unsubsribed from | False if channel was already empty or failed
clear_channel(channel: Int!): Boolean!
```

## API Scheme

```graphql
type Query {
  points(viewport: Viewport!): [DataPoint!]
  channels: [String]!
  datasets: [String]!
}

type Mutation {
  set_channel(channel: Int!, data_set: String!): DataSet!
  clear_channel(channel: Int!): Boolean!
}

type DataPoint {
  lon: Float!
  lat: Float!
  value1: Float!
	value2: Float
}

type DataSet {
  name: String
  display_type: String
  color_set: String
  min_val: Float
  max_val: Float
  error: String
}

input Viewport {
  lat1: Float!
  lon1: Float!
  lat2: Float!
  lon2: Float!
  interval: Float!
}
```