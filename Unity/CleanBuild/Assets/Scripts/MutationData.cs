using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

namespace mutation
{
    [Serializable]
    public class MutationData
    {

        public float min_val;
        public float max_val;


        public MutationData(float minVal, float maxVal)
        {
            min_val = minVal;
            max_val = maxVal;
        }

    }
}
