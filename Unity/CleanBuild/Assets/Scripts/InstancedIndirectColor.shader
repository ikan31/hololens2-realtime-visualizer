Shader "Custom/InstancedIndirectColor" {

    SubShader {
        Tags { "RenderType" = "Transparent" }
        Blend SrcAlpha OneMinusSrcAlpha
        Pass {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            #include "UnityCG.cginc"
            
            struct appdata_t {
                float4 vertex   : POSITION;
                float4 color    : COLOR;
               //UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct v2f {
                float4 vertex   : SV_POSITION;
                fixed4 color    : COLOR;
                //UNITY_VERTEX_OUTPUT_STEREO
            }; 

            struct MeshProperties {
                float4x4 mat;
                float4 color;
            };

            StructuredBuffer<MeshProperties> _Properties;
            float4x4 _EarthPos;
            float4x4 _EarthRot;
            float4x4 _EarthScale;

            v2f vert(appdata_t i, uint instanceID: SV_InstanceID) {
                v2f o;
                //UNITY_SETUP_INSTANCE_ID(i);
                //UNITY_INITIALIZE_OUTPUT(v2f, o); 
                //UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(o); 

                float4x4 m = mul(_EarthScale, _Properties[instanceID].mat);
                m = mul(_EarthRot, m);
                m = mul(_EarthPos, m);
                float4 pos = mul(m, i.vertex);
                o.vertex = UnityObjectToClipPos(pos);
                o.color = _Properties[instanceID].color;

                return o;
            }
            
            fixed4 frag(v2f i) : SV_Target {
                return i.color;
            }
            
            ENDCG
        }
    }
}