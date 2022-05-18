import json
import pytest
import time
from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def set_channel(client, channel_set):
    query = """
             mutation {
              set_channel(channel: 0, data_set : \"""" + f"{channel_set}" + """\") {
                name
                display_type
                color_set
                min_val
                max_val
                error
              }
            }"""
    response = client.post("/graphql", json={"query": query})
    return response


def get_view(client, lat1, lon1, lat2, lon2, inter):
    view = f"lat1 : {lat1}, lon1 :{lon1}, lat2:{lat2},lon2:{lon2},interval:{inter}"
    query = """
                 query {
                  points(viewport : {""" + view + """},channel: 0) {
                    lat
                    lon
                    value
                  }
                }"""
    response = client.post("/graphql", json={"query": query})
    return response


# Tests that we can set and call a data set with no unexpected errors or values, logs response rate
def generic_test(client, channel):
    response = set_channel(client, channel)
    assert response.json["data"]["set_channel"]["error"] == None
    dataset = response.json["data"]["set_channel"]
    #dataset is defined
    for i in dataset.keys():
        assert dataset[i] != None
    start = time.perf_counter()
    response = get_view(client, 1, 1, 2, 2, 1)
    print(time.perf_counter() - start, " response time")
    data = response.json["data"]["points"]
    # returned values are in range
    for i in data:
        assert dataset["min_val"] <= i and dataset["max_val"] >= i


def test_openweather_temp(client):
    generic_test(client, "openweather_temp")


def test_openweather_humidity(client):
    generic_test(client, "openweather_humidity")


def test_openweather_pressure(client):
    generic_test(client, "openweather_pressure")
