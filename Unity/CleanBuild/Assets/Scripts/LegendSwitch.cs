using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LegendSwitch : MonoBehaviour
{
    Renderer m_Renderer;
    private Texture2D myGUITexture;

    // Start is called before the first frame update
    void Start()
    {
        m_Renderer = GetComponent<Renderer>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void switchLegend(string dataType)
    {
        if(dataType.Length < 1)
        {
            myGUITexture = (Texture2D)Resources.Load("empty");
        }
        else
        {
            myGUITexture = (Texture2D)Resources.Load(dataType);
        }

        m_Renderer.material.SetTexture("_MainTex", myGUITexture);
    }
}
