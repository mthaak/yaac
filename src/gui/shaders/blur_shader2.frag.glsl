#version 330
//from https://www.shadertoy.com/view/XdfGDH

uniform vec3      iResolution;           // viewport resolution (in pixels)
uniform float     iGlobalTime;           // shader playback time (in seconds)
uniform float     iTimeDelta;            // render time (in seconds)
uniform int       iFrame;                // shader playback frame
uniform float     iChannelTime[4];       // channel playback time (in seconds)
uniform vec3      iChannelResolution[4]; // channel resolution (in pixels)
uniform vec4      iMouse;                // mouse pixel coords. xy: current (if MLB down), zw: click
uniform sampler2D iChannel0;             // input channel. XX = 2D/Cube
uniform vec4      iDate;                 // (year, month, day, time in seconds)
uniform float     iSampleRate;           // sound sample rate (i.e., 44100)

uniform float     radius;                // radius of blur
uniform sampler2D foregroundTexture;
uniform bool      useFG;

float SCurve (float x) {
    x = x * 2.0 - 1.0;
    return -x * abs(x) * 0.5 + x + 0.5;

//        return dot(vec3(-x, 2.0, 1.0 ),vec3(abs(x), x, 1.0)) * 0.5; // possibly faster version

}

vec4 BlurV (sampler2D source, vec2 size, vec2 uv, float radius) {
    // Hack such that edges are not blurred
    bool isEdge = texture(source, uv).r == 0.015; // specific red

	if (radius >= 1.0 && !isEdge)
	{
		vec4 A = vec4(0.0);
		vec4 C = vec4(0.0);
		vec4 FG = vec4(0.0);

		float height = 1.0 / size.y;

		float divisor = 0.0;
		float a_divisor = 0.0;
        float weight = 0.0;

        float radiusMultiplier = 1.0 / radius;

        for (float y = -radius; y <= radius; y++)
		{
			A = texture(source, uv + vec2(0.0, y * height));
			FG = texture(foregroundTexture, uv + vec2(0.0, y * height));

            if (uv.y + y * height >= 0) {

                weight = SCurve(1.0 - (abs(y) * radiusMultiplier));

                if (A.a > 0) {
                    C.r += A.r * weight;
                    C.g += A.g * weight;
                    C.b += A.b * weight;
                    divisor += weight;
                }
                if (!useFG || FG.a == 0) {
                    C.a += A.a * weight;
                    a_divisor += weight;
                }

            }
		}

		return vec4(C.r / divisor, C.g / divisor, C.b / divisor, C.a / a_divisor);
	}

	return texture(source, uv);
}



void main()
{
    vec2 uv = gl_FragCoord.xy / iResolution.xy;

    // Apply vertical blur to buffer A
	gl_FragColor = BlurV(iChannel0, iResolution.xy, uv, radius);
}