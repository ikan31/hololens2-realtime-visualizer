using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using DataFormat;
using System.IO;
using System.Linq;
using jsonHelp;
using DataProperties;
using drawMeshes;
using Microsoft.MixedReality.Toolkit;

namespace visuals
{
   
    public class BasicComputeSpheres : MonoBehaviour
    {
        private Dictionary<String, Gradient> colorKeys;
        public float intervalSize = 0.08f;

        public Material material;

        private ComputeBuffer meshPropertiesBuffer;
        private ComputeBuffer argsBuffer;

        private Mesh mesh;
        private Bounds bounds;
        private Data[] tData; 
        private bool visualsOn = false;
        float earthRadius = 1.03f; //radius in km
        Transform earthTransform;

        Dictionary<String, Vector2> minMax;
        Dictionary<String, DataInfo> dataInfos;

        private struct MeshProperties
        {
            public Matrix4x4 mat;
            public Vector4 color;
            public static int Size()
            {
                return
                    sizeof(float) * 4 * 4 + // matrix;
                    sizeof(float) * 4;   // color;
            }
        }

        private void Setup()
        {
            Mesh mesh = CreateQuad();
            this.mesh = mesh;
            // Boundary surrounding the meshes we will be drawing.  Used for occlusion.
            bounds = new Bounds(transform.position,  3f * Vector3.one);

        }

        void Start()
        {           
            colorKeys = setColorData();
            dataInfos = new Dictionary<string, DataInfo>();
            minMax = new Dictionary<string, Vector2>();
            minMax["openweather_temp"] = new Vector2(0, 100);
            minMax["openweather_humidity"] = new Vector2(0, 100);
            minMax["openweather_pressure"] = new Vector2(1000, 1016);
            minMax["Life expectancy at birth (years)"] = new Vector2(50, 80);
            Setup();
        }

        Vector3 convertSphericalToCartesian(float latitude, float longitude)
        {
            var lat = DegtoRad(latitude);
            var lon = DegtoRad(longitude);
            var x = (1.03f) * Math.Cos(lat) * Math.Cos(lon);
            var y = (1.03f) * Math.Cos(lat) * Math.Sin(lon);
            var z = (1.03f) * Math.Sin(lat);
            return new Vector3((float)x, (float)z, (float)y);
        }

        public static double DegtoRad(double degrees)
        {
            double radians = (Math.PI / 180) * degrees;
            return (radians);
        }
        public void clearButton()
        {
            visualsOn = false;
        }

        public void centerView()
        {
            transform.position = Camera.main.transform.position;
            transform.position = new Vector3(transform.position.x, transform.position.y + 0.5f, transform.position.z);
            transform.rotation = Quaternion.Euler(0, 0, 0);
            transform.localScale = 0.3f * Vector3.one;

        }
        void Update()
        {
            if (visualsOn)
            {
                material.SetMatrix("_EarthPos", Matrix4x4.Translate(transform.position));
                material.SetMatrix("_EarthRot", Matrix4x4.Rotate(transform.rotation));
                material.SetMatrix("_EarthScale", Matrix4x4.Scale(transform.localScale));
                Graphics.DrawMeshInstancedIndirect(mesh, 0, material, bounds, argsBuffer);
            }
        }

        void OnDestroy()
        {
            //resultBuffer.Dispose();
        }

        private void OnDisable()
        {
            // Release gracefully.
            if (meshPropertiesBuffer != null)
            {
                meshPropertiesBuffer.Release();
            }
            meshPropertiesBuffer = null;

            if (argsBuffer != null)
            {
                argsBuffer.Release();
            }
            argsBuffer = null;
        }

        private void InitializeBuffers(Data[] tData, string typename)
        {
            int population = tData.Length;
            if (population < 1)
                return;
            // Argument buffer used by DrawMeshInstancedIndirect.
            uint[] args = new uint[5] { 0, 0, 0, 0, 0 };
            // Arguments for drawing mesh.
            args[0] = (uint)mesh.GetIndexCount(0);
            args[1] = (uint)population;
            args[2] = (uint)mesh.GetIndexStart(0);
            args[3] = (uint)mesh.GetBaseVertex(0);
            argsBuffer = new ComputeBuffer(1, args.Length * sizeof(uint), ComputeBufferType.IndirectArguments);
            argsBuffer.SetData(args);

            // Initialize buffer with the given population.
            MeshProperties[] properties = new MeshProperties[population];
            float scaledValue = 0f;
            for (int i = 0; i < population; i++)
            {
                scaledValue = (tData[i].value1 - minMax[dataInfos[typename].typeName].x) / (minMax[dataInfos[typename].typeName].y - minMax[dataInfos[typename].typeName].x);
                Vector3 sphereCoord = convertSphericalToCartesian(tData[i].lat, tData[i].lon);
                MeshProperties props = new MeshProperties();
                props.mat = Matrix4x4.TRS(sphereCoord, Quaternion.LookRotation(-sphereCoord), intervalSize *  Vector3.one);
                props.color = colorKeys[dataInfos[typename].typeName].Evaluate(scaledValue);

                properties[i] = props;
            }

            meshPropertiesBuffer = new ComputeBuffer(population, MeshProperties.Size());
            meshPropertiesBuffer.SetData(properties);
            material.SetBuffer("_Properties", meshPropertiesBuffer);
            visualsOn = true;
        }
       
        public void switch_layout(string jsonString, string dataType)
        {
            try
            {
                tData = JsonHelper.FromJson<Data>(jsonString);

            }
            catch (Exception)
            {
                Debug.Log("Error fetching data");
                return;
            }
            dataInfos[dataType] = new DataInfo(dataType);
            InitializeBuffers(tData, dataType);
        }

        private static Dictionary<String, Gradient> setColorData()
        {

            Dictionary<String, Gradient> Pairs = new Dictionary<String, Gradient>();
            GradientAlphaKey[] alphaKey = new GradientAlphaKey[1];
            alphaKey[0].alpha = 0.55f;
            alphaKey[0].time = 0.0f;

            //Temperature
            Pairs["openweather_temp"] = new Gradient();
            GradientColorKey[] colorKey = new GradientColorKey[5];
            colorKey[0].color = new Color(1f, 0f, 1f);
            colorKey[0].time = 0.0f;
            colorKey[1].color = new Color(0f, 0.812f, 0.882f);
            colorKey[1].time = 0.25f;
            colorKey[2].color = new Color(0.392f, 0.745f, 0f);
            colorKey[2].time = 0.50f;
            colorKey[3].color = new Color(1f, 1f, 0f);
            colorKey[3].time = 0.75f;
            colorKey[4].color = new Color(1f, 0f, 0f);
            colorKey[4].time = 1.0f;
            Pairs["openweather_temp"].SetKeys(colorKey, alphaKey);


            //Humidity
            Pairs["openweather_humidity"] = new Gradient();
            colorKey[0].color = new Color(1f, 0f, 0f);
            colorKey[0].time = 0.0f;
            colorKey[1].color = new Color(1f, 0.6f, 0f);
            colorKey[1].time = 0.25f;
            colorKey[2].color = new Color(0.572f, 0.72f, 0.815f);
            colorKey[2].time = 0.50f;
            colorKey[3].color = new Color(0.219f, 0.462f, 0.113f);
            colorKey[3].time = 0.75f;
            colorKey[4].color = new Color(0.109f, 0.27f, 0.529f);
            colorKey[4].time = 1.0f;
            Pairs["openweather_humidity"].SetKeys(colorKey, alphaKey);


            //Pressure
            Pairs["openweather_pressure"] = new Gradient();
            colorKey[0].color = new Color(0.612f, 0.475f, 0.337f);
            colorKey[0].time = 0.0f;
            colorKey[1].color = new Color(0.898f, 0.835f, 0.776f);
            colorKey[1].time = 0.25f;
            colorKey[2].color = new Color(0.529f, 0.820f, 0.937f);
            colorKey[2].time = 0.50f;
            colorKey[3].color = new Color(0.247f, 0.772f, 0.984f);
            colorKey[3].time = 0.75f;
            colorKey[4].color = new Color(0f, 0.525f, 0.737f);
            colorKey[4].time = 1.0f;
            Pairs["openweather_pressure"].SetKeys(colorKey, alphaKey);


            //Life Expectancy
            Pairs["Life expectancy at birth (years)"] = new Gradient();
            colorKey[0].color = new Color(1f, 0f, 0f);
            colorKey[0].time = 0.0f;
            colorKey[1].color = new Color(1f, 0.6f, 0f);
            colorKey[1].time = 0.25f;
            colorKey[2].color = new Color(1f, 1f, 0f);
            colorKey[2].time = 0.50f;
            colorKey[3].color = new Color(0.572f, 0.72f, 0.815f);
            colorKey[3].time = 0.75f;
            colorKey[4].color = new Color(0.219f, 0.462f, 0.113f);
            colorKey[4].time = 1.0f;
            Pairs["Life expectancy at birth (years)"].SetKeys(colorKey, alphaKey);

            return Pairs;
        }

        private Mesh CreateQuad(float width = 0.3f, float height = 0.3f)
        {
            // Create a quad mesh.
            var mesh = new Mesh();

            float w = width * .5f;
            float h = height * .5f;
            var vertices = new Vector3[4] {
            new Vector3(-w, -h, 0),
            new Vector3(w, -h, 0),
            new Vector3(-w, h, 0),
            new Vector3(w, h, 0)
        };

            var tris = new int[6] {
            // lower left tri.
            0, 2, 1,
            // lower right tri
            2, 3, 1
        };

            var normals = new Vector3[4] {
            -Vector3.forward,
            -Vector3.forward,
            -Vector3.forward,
            -Vector3.forward,
        };

            var uv = new Vector2[4] {
            new Vector2(0, 0),
            new Vector2(1, 0),
            new Vector2(0, 1),
            new Vector2(1, 1),
        };

            mesh.vertices = vertices;
            mesh.triangles = tris;
            mesh.normals = normals;
            mesh.uv = uv;

            return mesh;
        }


        private List<Data> interpolate(Data[] tData)
        {
            List<Data> InterpolatedData = new List<Data>();

            List<Data> lonSorted = tData.OrderBy(x => x.lon).ThenBy(x => x.lat).ToList<Data>();
            for (int i = 0; i < tData.Length - 1; i++)
            {
                if (lonSorted[i].lon != lonSorted[i + 1].lon)
                {
                    continue;
                }
                Data point = new Data(
                    (lonSorted[i].lat + lonSorted[i + 1].lat) / 2,
                    (lonSorted[i].lon + lonSorted[i + 1].lon) / 2,
                    (lonSorted[i].value1 + lonSorted[i + 1].value1) / 2,
                    (lonSorted[i].value2 + lonSorted[i + 1].value2) / 2);

                InterpolatedData.Add(point);
                InterpolatedData.Add(lonSorted[i]);
            }

            List<Data> latSorted = InterpolatedData.OrderBy(x => x.lat).ThenBy(x => x.lon).ToList<Data>();
            for (int i = 0; i < latSorted.Count - 1; i++)
            {
                if (latSorted[i].lat != latSorted[i + 1].lat)
                {
                    continue;
                }

                Data point = new Data(
                     (latSorted[i].lat + latSorted[i + 1].lat) / 2,
                     (latSorted[i].lon + latSorted[i + 1].lon) / 2,
                     (latSorted[i].value1 + latSorted[i + 1].value1) / 2,
                     (latSorted[i].value2 + latSorted[i + 1].value2) / 2);

                InterpolatedData.Add(point);
            }
            return InterpolatedData;
        }
    }

}