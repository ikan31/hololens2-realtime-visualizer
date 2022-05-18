from distutils.log import debug
import importlib
import os
import json
import time
import openweather_requests as open
import who_athena as who

from ariadne import graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify

from api_scheme import *

apiDict = {}
dataDict = {}
dataDef = {}

def create_app():
    files = os.listdir()
    reserved = ["app.py", "apptest.py", "main.py",
                "api_scheme.py", "openweather_helper.py"]
    for i in files:
        if len(i) > 3 and i[len(i) - 3:] == ".py" and i not in reserved:
            print(i, " imported")
            apiDict[i[:len(i) - 3]] = importlib.import_module(i[:len(i) - 3])
        elif len(i) > 5 and i[len(i) - 5:] == ".json":
            # update dataDict here
            dataconfig = json.load(open(i))
            name = dataconfig["name"]
            for j in dataconfig["datasets"]:
                key = ""
                for k in j.keys():
                    key = k
                    tdict = j[k]
                    va = (tdict["display_type"], tdict["color_set"],
                          tdict["min_val"], tdict["max_val"])
                dataDict[key] = name
                dataDef[key] = va


query = QueryType()
mutation = MutationType()

 # num_channels = 3
channels = [None, None, None]

datasets_available = ["openweather_wind", "openweather_humidity", "openweather_temp", "openweather_pressure", "Life expectancy at birth (years)"]

@query.field('channels')
def resolve_channels(*_):
    return channels


@query.field('datasets')
def resolve_datasets(*_):
    return datasets_available


@mutation.field('set_channel')
def resolve_set_channel(*_, channel, data_set):
    if data_set in datasets_available:
        channels[channel] = None
        channels[channel] = data_set
    else:
        return {'error': f'{data_set} : is not available'}

    return channels

@mutation.field('clear_channel')
def resolve_clear_channel(*_, channel):
    if (channels[channel] == None):
        return False

    channels[channel] = None
    return True

@query.field('points')
def resolve_points(*_, viewport, channel, year = None):
    print("\nRequesting Data..\n")
    start = time.perf_counter()
    if (channels == [None, None, None]):
        return []
    dstream = channels[channel]
    # module = apiDict[dataDict[dstream]]
    # Realtime Data
    if year == None:
        res = open.data(dstream, viewport)
    # Historical Data
    else:
        res = who.data(dstream, viewport, year)

    print('\n-----------------\n')
    print('Time to return data: {}'.format(time.perf_counter() - start))
    print('Number of data points: {}'.format(len(res)))
    print('\n-----------------\n')

    return res
    

schema = make_executable_schema(type_defs, query, mutation)

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host='sdmay22-21.ece.iastate.edu', port=5000)
    # app.run(host='sdmay22-21.ece.iastate.edu')
