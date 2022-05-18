using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace DataProperties
{
    // Start is called before the first frame update
    [Serializable]
    public class DataInfo
    {

        public String typeName;
        public float min;
        public float max;
        public GameObject[] instances;
        public Gradient gradient;

        public DataInfo(String t) {
            typeName = t;
        }

        public DataInfo(String t, float mi, float ma)
        {
            typeName = t;
            min = mi;
            max = ma;
        }

    }
}
