using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;
using visuals;
using mutation;
using DataProperties;
using System.Collections.Generic;

// UnityWebRequest.Get example

// Access a website and use UnityWebRequest.Get to download a page.
// Also try to download a non-existing page. Display the error.

public class ServerRequests : MonoBehaviour
{
    BasicComputeSpheres compute;
    private Dictionary<string, int> channelMap;
    void Start()
    {
        channelMap = new Dictionary<string, int>();
        channelMap["openweather_temp"] = 0;
        channelMap["openweather_humidity"] = 1;
        channelMap["openweather_pressure"] = 2;
        channelMap["Life expectancy at birth (years)"] = 0;
        compute = GetComponent<BasicComputeSpheres>();
    }

    public void fetch(string dataType)
    {
        
        compute.intervalSize = 0.1f;
        int channel = channelMap[dataType];
        string query = @"{""query"" : ""{points(viewport: { lat1: -90, lon1: -180, lat2: 90, lon2: 180, interval: 10.0 }, channel: " + channel + @") { lat lon value1 value2 }}""}";

        StartCoroutine(MutateFetch(channel, dataType, query));
    }

    public void historical_fetch(string dataType)
    {
        compute.intervalSize = 0.3f;
        int channel = channelMap[dataType];
        string query = @"{""query"" : ""{points(viewport: { lat1: -90, lon1: -180, lat2: 90, lon2: 180, interval: 1.0 }, channel: " + channel + ", year: \\\"2019\\\") {\\r\\n  \\tlat\\r\\n    lon\\r\\n    value1\\r\\n  }\\r\\n}\\r\\n\\r\\n\\r\\n\",\"variables\":{}}";
        Debug.Log(query);
        StartCoroutine(MutateFetch(channel, dataType, query));
    }

    IEnumerator Post(string url, string bodyJsonString, System.Action<string> callback)
    {
        var request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = Encoding.UTF8.GetBytes(bodyJsonString);
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.Send();
        callback(request.downloadHandler.text);
        //Debug.Log("Status Code: " + request.downloadHandler.text);

    }

    IEnumerator MutateFetch(int channel, string dataType, string query)
    {
        //string mutateQuery = @"{""mutation"" : ""{set_channel(channel: 0, data_set: ""openweather_temp"") { name display_type color_set min_val max_val error }}""}";
        //string mutateQuery = "{\"query\":\"mutation {set_channel(channel: " + channel +", data_set: \\\" "+ dataType +"\\\") {\\r\\n min_val\\r\\n    max_val\\r\\n }\\r\\n}\\r\\n\\r\\n\",\"variables\":{}}";
        string mutateQuery = "{\"query\":\"mutation {\\r\\n  set_channel(channel: " + channel + ", data_set: \\\"" + dataType + "\\\") {\\r\\n    min_val\\r\\n    max_val\\r\\n  }\\r\\n}\\r\\n\\r\\n\",\"variables\":{}}";
        string data = "";
        yield return Post("http://sdmay22-21.ece.iastate.edu:5000/graphql", mutateQuery, (value) =>
        {

            Debug.Log("mutate ran: " + value);

        });

        //string query = @"{""query"" : ""{points(viewport: { lat1: 40.2, lon1: -93.2, lat2: 43.5, lon2: -92.5, interval: 1.0 }, channel: 0) { lat lon value }}""}";
        
        yield return Post("http://sdmay22-21.ece.iastate.edu:5000/graphql", query, (value) =>
        {
            data = value;
            char[] start = { '{' };
            data = data.TrimStart(start);
            data = data.Replace(@"""data"":", "");
            char[] end = { '}', ' ', '\n' };
            data = data.TrimEnd(end);
            data = data + "}";

            Debug.Log(data);
            GetComponent<BasicComputeSpheres>().switch_layout(data, dataType);
        });
    }

}