using Silk.NET.OpenGL;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using StbImageSharp;
using Silk.NET.Maths;
using System.Globalization;
using System.Reflection;

namespace project
{
    internal class ModelObjectDescriptor
    {
        public uint Vao { get; private set; }
        public uint Vertices { get; private set; }
        public uint Colors { get; private set; }
        public uint? Texture { get; private set; } = new uint?();
        public uint Indices { get; private set; }
        public uint IndexArrayLength { get; private set; }

        private GL Gl;

        public static unsafe ModelObjectDescriptor CreateGround(GL Gl)
        {
            //the ground will be size*size units, centered around the origin, forming a square on the XZ plane

            float size = 100f;
            float[] vertexArray = new float[]
            {
                //  Position        Normal        TexCoord
                -size, 0f, -size,   0f, 1f, 0f,   0f, 0f,
                 size, 0f, -size,   0f, 1f, 0f,   1f, 0f,
                 size, 0f,  size,   0f, 1f, 0f,   1f, 1f,
                -size, 0f,  size,   0f, 1f, 0f,   0f, 1f,
            };

            float[] colorArray = new float[]
            {
                0f, 0.8f, 0f, 1f,
                0f, 0.8f, 0f, 1f,
                0f, 0.8f, 0f, 1f,
                0f, 0.8f, 0f, 1f,
            };

            uint[] indexArray = new uint[]
            {
                0, 1, 2,
                0, 2, 3
            };

            return CreateObjectDescriptorFromArrays(Gl, vertexArray, colorArray, indexArray);
        }
      
        public unsafe static ModelObjectDescriptor CreateSkyBox(GL Gl)
        {
            // counter clockwise is front facing
            // vx, vy, vz, nx, ny, nz, tu, tv
            float[] vertexArray = new float[] {
                // top face
                -0.5f, 0.5f, 0.5f, 0f, -1f, 0f, 1f/4f, 0f/3f,
                0.5f, 0.5f, 0.5f, 0f, -1f, 0f, 2f/4f, 0f/3f,
                0.5f, 0.5f, -0.5f, 0f, -1f, 0f, 2f/4f, 1f/3f,
                -0.5f, 0.5f, -0.5f, 0f, -1f, 0f, 1f/4f, 1f/3f,

                // front face
                -0.5f, 0.5f, 0.5f, 0f, 0f, -1f, 1, 1f/3f,
                -0.5f, -0.5f, 0.5f, 0f, 0f, -1f, 4f/4f, 2f/3f,
                0.5f, -0.5f, 0.5f, 0f, 0f, -1f, 3f/4f, 2f/3f,
                0.5f, 0.5f, 0.5f, 0f, 0f, -1f,  3f/4f, 1f/3f,

                // left face
                -0.5f, 0.5f, 0.5f, 1f, 0f, 0f, 0, 1f/3f,
                -0.5f, 0.5f, -0.5f, 1f, 0f, 0f,1f/4f, 1f/3f,
                -0.5f, -0.5f, -0.5f, 1f, 0f, 0f, 1f/4f, 2f/3f,
                -0.5f, -0.5f, 0.5f, 1f, 0f, 0f, 0f/4f, 2f/3f,

                // bottom face
                -0.5f, -0.5f, 0.5f, 0f, 1f, 0f, 1f/4f, 1f,
                0.5f, -0.5f, 0.5f,0f, 1f, 0f, 2f/4f, 1f,
                0.5f, -0.5f, -0.5f,0f, 1f, 0f, 2f/4f, 2f/3f,
                -0.5f, -0.5f, -0.5f,0f, 1f, 0f, 1f/4f, 2f/3f,

                // back face
                0.5f, 0.5f, -0.5f, 0f, 0f, 1f, 2f/4f, 1f/3f,
                -0.5f, 0.5f, -0.5f, 0f, 0f, 1f, 1f/4f, 1f/3f,
                -0.5f, -0.5f, -0.5f,0f, 0f, 1f, 1f/4f, 2f/3f,
                0.5f, -0.5f, -0.5f,0f, 0f, 1f, 2f/4f, 2f/3f,

                // right face
                0.5f, 0.5f, 0.5f, -1f, 0f, 0f, 3f/4f, 1f/3f,
                0.5f, 0.5f, -0.5f,-1f, 0f, 0f, 2f/4f, 1f/3f,
                0.5f, -0.5f, -0.5f, -1f, 0f, 0f, 2f/4f, 2f/3f,
                0.5f, -0.5f, 0.5f, -1f, 0f, 0f, 3f/4f, 2f/3f,
            };

            float[] colorArray = new float[] {
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,

                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,

                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,

                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,

                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,

                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
                0.0f, 0.0f, 0.0f, 1.0f,
            };

            uint[] indexArray = new uint[] {
                0, 2, 1,
                0, 3, 2,

                4, 6, 5,
                4, 7, 6,

                8, 10, 9,
                10, 8, 11,

                12, 13, 14,
                12, 14, 15,

                17, 19, 16,
                17, 18, 19,

                20, 21, 22,
                20, 22, 23
            };

            var skyboxImage = ReadTextureImage("skybox.png");

            return CreateObjectDescriptorFromArrays(Gl, vertexArray, colorArray, indexArray, skyboxImage);
        }

        public static ModelObjectDescriptor CreateAnimalFromObj(GL Gl)
        {
            List<float[]> objVertices = new List<float[]>();
            List<int[]> objFaces = new List<int[]>();

            string fullResourceName = "project.Resources.teapot.obj";
            using (var objStream = Assembly.GetExecutingAssembly().GetManifestResourceStream(fullResourceName))
            using (var objReader = new StreamReader(objStream))
            {
                while (!objReader.EndOfStream)
                {
                    var line = objReader.ReadLine();

                    if (string.IsNullOrWhiteSpace(line))
                        continue;

                    var lineClassifier = line.Substring(0, line.IndexOf(' '));
                    var lineData = line.Substring(line.IndexOf(" ")).Trim().Split(' ');

                    switch (lineClassifier)
                    {
                        case "v":
                            float[] vertex = new float[3];
                            for (int i = 0; i < vertex.Length; ++i)
                                vertex[i] = float.Parse(lineData[i], CultureInfo.InvariantCulture);
                            objVertices.Add(vertex);
                            break;
                        case "f":
                            int[] face = new int[3];
                            for (int i = 0; i < face.Length; ++i)
                                face[i] = int.Parse(lineData[i], CultureInfo.InvariantCulture);
                            objFaces.Add(face);
                            break;
                        default:
                            throw new Exception("Unhandled obj structure.");
                    }
                }
            }

            List<ObjVertexTransformationData> vertexTransformations = new List<ObjVertexTransformationData>();
            foreach (var objVertex in objVertices)
            {
                vertexTransformations.Add(new ObjVertexTransformationData(
                    new Vector3D<float>(objVertex[0], objVertex[1], objVertex[2]),
                    Vector3D<float>.Zero,
                    0
                    ));
            }

            foreach (var objFace in objFaces)
            {
                var a = vertexTransformations[objFace[0] - 1];
                var b = vertexTransformations[objFace[1] - 1];
                var c = vertexTransformations[objFace[2] - 1];

                var normal = Vector3D.Normalize(Vector3D.Cross(b.Coordinates - a.Coordinates, c.Coordinates - a.Coordinates));

                a.UpdateNormalWithContributionFromAFace(normal);
                b.UpdateNormalWithContributionFromAFace(normal);
                c.UpdateNormalWithContributionFromAFace(normal);
            }


            List<float> glVertices = new List<float>();
            List<float> glColors = new List<float>();
            foreach (var vertexTransformation in vertexTransformations)
            {
                glVertices.Add(vertexTransformation.Coordinates.X);
                glVertices.Add(vertexTransformation.Coordinates.Y);
                glVertices.Add(vertexTransformation.Coordinates.Z);

                glVertices.Add(vertexTransformation.Normal.X);
                glVertices.Add(vertexTransformation.Normal.Y);
                glVertices.Add(vertexTransformation.Normal.Z);

                glColors.AddRange([1.0f, 0.0f, 0.0f, 1.0f]);
            }

            List<uint> glIndexArray = new List<uint>();
            foreach (var objFace in objFaces)
            {
                glIndexArray.Add((uint)(objFace[0] - 1));
                glIndexArray.Add((uint)(objFace[1] - 1));
                glIndexArray.Add((uint)(objFace[2] - 1));
            }

            return CreateObjectDescriptorFromArrays(Gl, glVertices.ToArray(), glColors.ToArray(), glIndexArray.ToArray(), null, false);
        }

        private static unsafe ModelObjectDescriptor CreateObjectDescriptorFromArrays(GL Gl, float[] vertexArray, float[] colorArray, uint[] indexArray,
           ImageResult textureImage = null, bool hasTexture = true)
        {
            uint vao = Gl.GenVertexArray();
            Gl.BindVertexArray(vao);

            uint vertices = Gl.GenBuffer();
            Gl.BindBuffer(GLEnum.ArrayBuffer, vertices);
            Gl.BufferData(GLEnum.ArrayBuffer, (ReadOnlySpan<float>)vertexArray.AsSpan(), GLEnum.StaticDraw);
            // 0 is position
            // 2 is normals
            // 3 is texture
            uint offsetPos = 0;
            uint offsetNormals = offsetPos + 3 * sizeof(float);
            uint offsetTexture = offsetNormals + 3 * sizeof(float);
            uint vertexSize=0;
            if (hasTexture)
            {   
               vertexSize = offsetTexture + 2 * sizeof(float);
            }
            else
            {
                vertexSize = offsetTexture + (textureImage == null ? 0u : 2 * sizeof(float));
            }
            

            Gl.VertexAttribPointer(0, 3, VertexAttribPointerType.Float, false, vertexSize, (void*)offsetPos);
            Gl.EnableVertexAttribArray(0);
            Gl.VertexAttribPointer(2, 3, VertexAttribPointerType.Float, true, vertexSize, (void*)offsetNormals);
            Gl.EnableVertexAttribArray(2);
            Gl.VertexAttribPointer(3, 2, VertexAttribPointerType.Float, false, vertexSize, (void*)offsetTexture);
            Gl.EnableVertexAttribArray(3);
            Gl.BindBuffer(GLEnum.ArrayBuffer, 0);


            uint colors = Gl.GenBuffer();
            Gl.BindBuffer(GLEnum.ArrayBuffer, colors);
            Gl.BufferData(GLEnum.ArrayBuffer, (ReadOnlySpan<float>)colorArray.AsSpan(), GLEnum.StaticDraw);
            // 1 is color
            Gl.VertexAttribPointer(1, 4, VertexAttribPointerType.Float, false, 0, null);
            Gl.EnableVertexAttribArray(1);
            Gl.BindBuffer(GLEnum.ArrayBuffer, 0);

            uint indices = Gl.GenBuffer();
            Gl.BindBuffer(GLEnum.ElementArrayBuffer, indices);
            Gl.BufferData(GLEnum.ElementArrayBuffer, (ReadOnlySpan<uint>)indexArray.AsSpan(), GLEnum.StaticDraw);
            Gl.BindBuffer(GLEnum.ElementArrayBuffer, 0);

            uint? texture = new uint?();

            if (textureImage != null)
            {
                // set texture
                // create texture
                texture = Gl.GenTexture();

                // activate texture 0
                Gl.ActiveTexture(TextureUnit.Texture0);
                // bind texture
                Gl.BindTexture(TextureTarget.Texture2D, texture.Value);
                // Here we use "result.Width" and "result.Height" to tell OpenGL about how big our texture is.
                Gl.TexImage2D(TextureTarget.Texture2D, 0, InternalFormat.Rgba, (uint)textureImage.Width,
                    (uint)textureImage.Height, 0, PixelFormat.Rgba, PixelType.UnsignedByte, (ReadOnlySpan<byte>)textureImage.Data.AsSpan());
                Gl.TexParameterI(TextureTarget.Texture2D, TextureParameterName.TextureWrapS, (int)TextureWrapMode.Repeat);
                Gl.TexParameterI(TextureTarget.Texture2D, TextureParameterName.TextureWrapT, (int)TextureWrapMode.Repeat);
                Gl.TexParameterI(TextureTarget.Texture2D, TextureParameterName.TextureMinFilter, (int)TextureMinFilter.Nearest);
                Gl.TexParameterI(TextureTarget.Texture2D, TextureParameterName.TextureMagFilter, (int)TextureMagFilter.Nearest);
                // unbinde texture
                Gl.BindTexture(TextureTarget.Texture2D, 0);
            }

            return new ModelObjectDescriptor() { Vao = vao, Vertices = vertices, Colors = colors, Indices = indices, IndexArrayLength = (uint)indexArray.Length, Gl = Gl, Texture = texture };
        }

        private static unsafe ImageResult ReadTextureImage(string textureResource)
        {
            ImageResult result;
            using (Stream skyeboxStream
                = typeof(ModelObjectDescriptor).Assembly.GetManifestResourceStream("project.Resources." + textureResource))
                result = ImageResult.FromStream(skyeboxStream, ColorComponents.RedGreenBlueAlpha);

            return result;
        }

        public static ModelObjectDescriptor CreateRedField(GL Gl, float size = 5f, float yOffset = 0.01f)
        {
            float[] vertexArray = new float[]
            {
                -size, yOffset, -size,   0f, 1f, 0f,   0f, 0f,
                 size, yOffset, -size,   0f, 1f, 0f,   1f, 0f,
                 size, yOffset,  size,   0f, 1f, 0f,   1f, 1f,
                -size, yOffset,  size,   0f, 1f, 0f,   0f, 1f,
            };

            float[] colorArray = new float[]
            {
                1f, 0f, 0f, 1f,
                1f, 0f, 0f, 1f,
                1f, 0f, 0f, 1f,
                1f, 0f, 0f, 1f,
            };

            uint[] indexArray = new uint[]
            {
                0, 1, 2,
                0, 2, 3
            };

            return CreateObjectDescriptorFromArrays(Gl, vertexArray, colorArray, indexArray);
        }

        public static unsafe ModelObjectDescriptor CreateAnimalWithTextureAndNormalsFromObj(GL Gl)
        {
            List<float[]> objVertices; //v
            List<float[]> objTexCoords; //vt
            List<float[]> objNormals; //vn
            List<(int v, int vt, int vn)[]> objFaces; ///f

            ReadObjDataFromResource("project.Resources.cat.obj", out objVertices, out objTexCoords, out objNormals, out objFaces);

            List<float> vertexArray = new();
            List<float> colorArray = new();
            List<uint> indexArray = new();

            Dictionary<(int, int, int), uint> uniqueVertexMap = new();
            uint currentIndex = 0;

            foreach (var face in objFaces)
            {
                foreach (var (v, vt, vn) in face)
                {
                    var key = (v, vt, vn);
                    if (!uniqueVertexMap.TryGetValue(key, out uint index))
                    {
                        float[] pos = objVertices[v - 1];
                        float[] tex = objTexCoords[vt - 1];
                        float[] norm = objNormals[vn - 1];

                        // Position
                        vertexArray.AddRange(pos); // x y z
                        // Normal
                        vertexArray.AddRange(norm); //nx ny nz
                        // TexCoord
                        vertexArray.AddRange(tex); // u v

                        // Color 
                        colorArray.AddRange(new float[] { 1f, 1f, 1f, 1f }); //white

                        uniqueVertexMap[key] = currentIndex;
                        index = currentIndex++;
                    }

                    indexArray.Add(index);
                }
            }

            return CreateObjectDescriptorFromArrays(Gl, vertexArray.ToArray(), colorArray.ToArray(), indexArray.ToArray(), null, hasTexture: true);
        }

        private static void ReadObjDataFromResource(string resourceName, out List<float[]> objVertices,out List<float[]> objTexCoords,out List<float[]> objNormals, out List<(int v, int vt, int vn)[]> objFaces)
        {
            objVertices = new();
            objTexCoords = new();
            objNormals = new();
            objFaces = new();

            using var objStream = typeof(ModelObjectDescriptor).Assembly.GetManifestResourceStream(resourceName)
                ?? throw new Exception($"Resource '{resourceName}' not found!");
            using var objReader = new StreamReader(objStream);

            while (!objReader.EndOfStream)
            {
                var line = objReader.ReadLine()?.Trim();
                if (string.IsNullOrWhiteSpace(line) || line.StartsWith("#"))
                    continue;

                var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
                if (parts.Length == 0)
                    continue;

                switch (parts[0])
                {
                    case "v":
                        objVertices.Add(parts[1..4].Select(s => float.Parse(s, CultureInfo.InvariantCulture)).ToArray());
                        break;
                    case "vt":
                        objTexCoords.Add(parts[1..3].Select(s => float.Parse(s, CultureInfo.InvariantCulture)).ToArray());
                        break;
                    case "vn":
                        objNormals.Add(parts[1..4].Select(s => float.Parse(s, CultureInfo.InvariantCulture)).ToArray());
                        break;
                    case "f":
                        var faceVertices = parts[1..].Select(p =>
                        {
                            var indices = p.Split('/');
                            return (
                                v: int.Parse(indices[0]),
                                vt: int.Parse(indices[1]),
                                vn: int.Parse(indices[2])
                            );
                        }).ToArray();

                        for (int i = 1; i < faceVertices.Length - 1; i++)
                        {
                            objFaces.Add(new[] {
                            faceVertices[0],
                            faceVertices[i],
                            faceVertices[i + 1]
                        });
                        }
                        break;
                }
            }
        }


    }
}
