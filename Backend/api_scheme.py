from ariadne import QueryType, MutationType, gql

type_defs = gql("""
    type Query {
        points(viewport: Viewport!, channel: Int!, year: String): [DataPoint!]!
        channels: [String]!
        datasets: [String]!
    }

    type Mutation {
        set_channel(channel: Int!, data_set: String!): DataSet!
        clear_channel(channel: Int!):  Boolean!
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
""")

query = QueryType()
mutation = MutationType()
