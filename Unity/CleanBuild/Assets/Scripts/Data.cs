using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

namespace DataFormat
{
    [Serializable]
    public class Data
    {
        public Data() { }


        public float lat;
        public float lon;
        public float value1;
        public float value2;


    public Data(float latT, float lonT, float valueT, float val2)
        {
            lat = latT;
            lon = lonT;
            value1 = valueT;
            value2 = val2;
        }

    }
}
