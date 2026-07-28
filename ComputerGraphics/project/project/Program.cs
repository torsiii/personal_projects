using Silk.NET.Maths;
using Silk.NET.OpenGL;
using System.Numerics;
using Silk.NET.OpenGL.Extensions.ImGui;
using System.Reflection;
using Silk.NET.Windowing;
using Silk.NET.Input;

namespace project
{
    internal class Program
    {
        private static IWindow graphicWindow;
        private static GL Gl;
        private static uint program;

        private static CameraDescriptor camera = new CameraDescriptor();
        private static CubeArrangementModel cubeArrangementModel = new CubeArrangementModel();
        private static ImGuiController imGuiController;

        private static ModelObjectDescriptor skybox;
        private static ModelObjectDescriptor ground;
        private static ModelObjectDescriptor animal;
        private static List<ModelObjectDescriptor> enemyTeapots = new();
        private static List<ModelObjectDescriptor> redFields = new();

        private static Vector3D<float> animalPosition = new(0f, 0f, 0f);
        private static List<Vector3D<float>> enemyPositions = new();
        private static List<Vector3D<float>> redFieldPositions = new();

        private const string TextureVariableName = "uTexture";
        private const string ModelMatrixVariableName = "uModel";
        private const string NormalMatrixVariableName = "uNormal";
        private const string LightColorVariableName = "uLightColor";
        private const string LightPositionVariableName = "uLightPos";
        private const string ViewPositionVariableName = "uViewPos";
        private const string ShinenessVariableName = "uShininess";
        private const string ViewMatrixVariableName = "uView";
        private const string ProjectionMatrixVariableName = "uProjection";
        private static float shininess = 50;
     
        private static float enemySpeed = 5f; // units per second
        private static bool gameOver = false;
        private static bool gameWon = false;
        private static List<bool> movingForwards = new();
        private static int collectedRedFieldCount = 0;
        private static bool catVisible = true;
        private static bool catViewEnabled = false;

        static void Main(string[] args)
        {
            WindowOptions windowOptions = WindowOptions.Default;
            windowOptions.Title = "project";
            windowOptions.Size = new Silk.NET.Maths.Vector2D<int>(500, 500);

            graphicWindow = Window.Create(windowOptions);

            graphicWindow.Load += GraphicWindow_Load;
            graphicWindow.Update += GraphicWindow_Update;
            graphicWindow.Render += GraphicWindow_Render;
            graphicWindow.Closing += GraphicWindow_Closing;

            graphicWindow.Run();
        }
        private static void GraphicWindow_Load()
        {
            // initializing opengl, loading models, compiling shaders and linking the program

            Gl = graphicWindow.CreateOpenGL();
            Gl.Enable(GLEnum.Blend);
            Gl.BlendFunc(BlendingFactor.SrcAlpha, BlendingFactor.OneMinusSrcAlpha);

            var inputContext = graphicWindow.CreateInput();

            ground = ModelObjectDescriptor.CreateGround(Gl);
            animal = ModelObjectDescriptor.CreateAnimalWithTextureAndNormalsFromObj(Gl);

            for (int i = 0; i < 3; i++)
            {
                enemyTeapots.Add(ModelObjectDescriptor.CreateAnimalFromObj(Gl));

                float startX = 40f + i * 10; // X positions
                enemyPositions.Add(new Vector3D<float>(startX, 0f, -10f + 10 * i)); // Z offset
                movingForwards.Add(true);
            }

            foreach (var keyboard in inputContext.Keyboards)
            {
                keyboard.KeyDown += Keyboard_KeyDown;
            }

            for (int i = 0; i < 3; i++) // red fiileds to collect
            {
                var x = Random.Shared.Next(-40, 40);
                var z = Random.Shared.Next(-40, 40);
                redFieldPositions.Add(new Vector3D<float>(x, 0f, z));
                redFields.Add(ModelObjectDescriptor.CreateRedField(Gl));
            }

            graphicWindow.FramebufferResize += s =>
            {
                Gl.Viewport(s);
            };

            imGuiController = new ImGuiController(Gl, graphicWindow, inputContext);
            skybox = ModelObjectDescriptor.CreateSkyBox(Gl);


            uint vshader = Gl.CreateShader(ShaderType.VertexShader);
            Gl.ShaderSource(vshader, GetEmbeddedResourceAsString("Shaders.VertexShader.vert"));
            Gl.CompileShader(vshader);
            Gl.GetShader(vshader, ShaderParameterName.CompileStatus, out int vStatus);
            if (vStatus != (int)GLEnum.True)
                throw new Exception("Vertex shader failed to compile: " + Gl.GetShaderInfoLog(vshader));

            uint fshader = Gl.CreateShader(ShaderType.FragmentShader);
            Gl.ShaderSource(fshader, GetEmbeddedResourceAsString("Shaders.FragmentShader.frag"));
            Gl.CompileShader(fshader);
            Gl.GetShader(fshader, ShaderParameterName.CompileStatus, out int fStatus);
            if (fStatus != (int)GLEnum.True)
                throw new Exception("Fragment shader failed to compile: " + Gl.GetShaderInfoLog(fshader));

            program = Gl.CreateProgram();
            Gl.AttachShader(program, vshader);
            Gl.AttachShader(program, fshader);
            Gl.LinkProgram(program);
            Gl.DeleteShader(vshader);
            Gl.DeleteShader(fshader);
        }
        private static void GraphicWindow_Update(double deltaTime)
        {
            if (gameOver)
                return;

            cubeArrangementModel.AdvanceTime(deltaTime);
            imGuiController.Update((float)deltaTime);

            for (int i = 0; i < enemyTeapots.Count; i++)
            {
                // enemy movement
                float movement = (float)(enemySpeed * deltaTime);
                if (movingForwards[i])
                    enemyPositions[i] = new Vector3D<float>(enemyPositions[i].X + movement, enemyPositions[i].Y, enemyPositions[i].Z);
                else
                    enemyPositions[i] = new Vector3D<float>(enemyPositions[i].X - movement, enemyPositions[i].Y, enemyPositions[i].Z);

                if (enemyPositions[i].X > 20f)
                    movingForwards[i] = false;
                else if (enemyPositions[i].X < -20f)
                    movingForwards[i] = true;

                if (Vector3D.Distance(animalPosition, enemyPositions[i]) < 2f && !gameOver) // checking collision
                {
                    gameOver = true;
                    catVisible = false;
                    Console.WriteLine("Game Over: You collided with an enemy teapot!");
                    Task.Delay(3000).ContinueWith(_ => Environment.Exit(0));
                }
            }


            // check if red squares were collected
            for (int i = redFieldPositions.Count - 1; i >= 0; i--)
            {
                if (i < redFieldPositions.Count && i < redFields.Count)
                {
                    var playerXZ = new Vector2D<float>(animalPosition.X, animalPosition.Z);
                    var redXZ = new Vector2D<float>(redFieldPositions[i].X, redFieldPositions[i].Z);

                    if (Vector2D.Distance(playerXZ, redXZ) < 5f)
                    {
                        redFieldPositions.RemoveAt(i);
                        redFields.RemoveAt(i);
                        collectedRedFieldCount++;
                    }
                }
            }

            if (redFieldPositions.Count == 0 && !gameWon)
            {
                gameWon = true;
                Console.WriteLine("You win! All red fields collected.");
                Task.Delay(3000).ContinueWith(_ => Environment.Exit(0));
            }
        }

        private static unsafe void GraphicWindow_Render(double deltaTime)
        {
            Gl.UseProgram(program);
            SetUniform3(LightColorVariableName, new Vector3(1f, 1f, 1f));
            SetUniform3(LightPositionVariableName, new Vector3(0f, 2f, 2f));
            SetUniform3(ViewPositionVariableName, new Vector3(camera.Position.X, camera.Position.Y, camera.Position.Z));
            SetUniform1(ShinenessVariableName, shininess);

            Matrix4X4<float> viewMatrix; //camera: cat view and default
            if (catViewEnabled)
            {
                var cameraPos = new Vector3D<float>(animalPosition.X, animalPosition.Y + 2f, animalPosition.Z - 5f);    // in front of cat
                var cameraTarget = new Vector3D<float>(animalPosition.X, animalPosition.Y + 1f, animalPosition.Z - 10f); // looking forward
                viewMatrix = Matrix4X4.CreateLookAt(cameraPos, cameraTarget, new Vector3D<float>(0f, 1f, 0f));
            }
            else
            {
                viewMatrix = Matrix4X4.CreateLookAt(camera.Position, camera.Target, camera.UpVector);
            }

            SetMatrix(viewMatrix, ViewMatrixVariableName);
            var projectionMatrix = Matrix4X4.CreatePerspectiveFieldOfView<float>((float)(Math.PI / 2), 1024f / 768f, 0.1f, 100f);
            SetMatrix(projectionMatrix, ProjectionMatrixVariableName);

            DrawSkyBox();

            SetModelMatrix(Matrix4X4.CreateTranslation(0f, -0.1f, 0f));
            DrawModelObject(ground);


            for (int i = 0; i < redFields.Count; i++)
            {
                var pos = redFieldPositions[i];
                var modelMatrixRed = Matrix4X4.CreateTranslation(pos.X, pos.Y, pos.Z);
                SetModelMatrix(modelMatrixRed);
                DrawModelObject(redFields[i]);
            }

            for (int i = 0; i < enemyTeapots.Count; i++)
            {
                var enemyModelMatrix = Matrix4X4.CreateTranslation(enemyPositions[i].X, enemyPositions[i].Y, enemyPositions[i].Z);
                SetModelMatrix(enemyModelMatrix);
                DrawModelObject(enemyTeapots[i]);
            }

            var scale = 0.25f;
            var rotation =Matrix4X4.CreateRotationX(-MathF.PI / 2)  // correct from Z-up to Y-up
                * Matrix4X4.CreateRotationY(MathF.PI);      // turn 180° around Y
            var animalModelMatrix =
                Matrix4X4.CreateScale(scale) * rotation *
                Matrix4X4.CreateTranslation(animalPosition.X, animalPosition.Y, animalPosition.Z);
            if (catVisible)
            {
                SetModelMatrix(animalModelMatrix);
                DrawModelObject(animal);
            }

            ImGuiNET.ImGui.Begin("Red Fields", ImGuiNET.ImGuiWindowFlags.AlwaysAutoResize | ImGuiNET.ImGuiWindowFlags.NoCollapse);
            ImGuiNET.ImGui.Text($"Collected: {collectedRedFieldCount}");
            ImGuiNET.ImGui.Checkbox("Cat View", ref catViewEnabled);
            ImGuiNET.ImGui.End();
            
            imGuiController.Render();
        }
        private static void GraphicWindow_Closing()
        {
            Gl.DeleteProgram(program);
        }

        private static unsafe void SetUniform3(string uniformName, Vector3 uniformValue)
        {
            int location = Gl.GetUniformLocation(program, uniformName);
            if (location == -1)
            {
                throw new Exception($"{uniformName} uniform not found on shader.");
            }

            Gl.Uniform3(location, uniformValue);
            CheckError();
        }

        private static unsafe void SetUniform1(string uniformName, float uniformValue)
        {
            int location = Gl.GetUniformLocation(program, uniformName);
            if (location == -1)
            {
                throw new Exception($"{uniformName} uniform not found on shader.");
            }

            Gl.Uniform1(location, uniformValue);
            CheckError();
        }
        private static unsafe void DrawSkyBox()
        {
            var modelMatrixSkyBox = Matrix4X4.CreateScale(100f);
            SetModelMatrix(modelMatrixSkyBox);

            // set the texture
            int textureLocation = Gl.GetUniformLocation(program, TextureVariableName);
         
            // set texture 0
            Gl.Uniform1(textureLocation, 0);
            Gl.ActiveTexture(TextureUnit.Texture0);
            Gl.TexParameter(TextureTarget.Texture2D, TextureParameterName.TextureMinFilter, (float)GLEnum.Linear);
            
            Gl.BindTexture(TextureTarget.Texture2D, skybox.Texture.Value);

            DrawModelObject(skybox);

            CheckError();
            Gl.BindTexture(TextureTarget.Texture2D, 0);
            CheckError();
        }

        private static unsafe void DrawModelObject(ModelObjectDescriptor modelObject)
        {
            Gl.BindVertexArray(modelObject.Vao);
            Gl.BindBuffer(GLEnum.ElementArrayBuffer, modelObject.Indices);
            Gl.DrawElements(PrimitiveType.Triangles, modelObject.IndexArrayLength, DrawElementsType.UnsignedInt, null);
            Gl.BindBuffer(GLEnum.ElementArrayBuffer, 0);
            Gl.BindVertexArray(0);
        }

        private static unsafe void SetModelMatrix(Matrix4X4<float> modelMatrix)
        {
            SetMatrix(modelMatrix, ModelMatrixVariableName);

            // set also the normal matrix
            int location = Gl.GetUniformLocation(program, NormalMatrixVariableName);
            if (location == -1)
            {
                throw new Exception($"{NormalMatrixVariableName} uniform not found on shader.");
            }

            // G = (M^-1)^T
            var modelMatrixWithoutTranslation = new Matrix4X4<float>(modelMatrix.Row1, modelMatrix.Row2, modelMatrix.Row3, modelMatrix.Row4);
            modelMatrixWithoutTranslation.M41 = 0;
            modelMatrixWithoutTranslation.M42 = 0;
            modelMatrixWithoutTranslation.M43 = 0;
            modelMatrixWithoutTranslation.M44 = 1;

            Matrix4X4<float> modelInvers;
            Matrix4X4.Invert<float>(modelMatrixWithoutTranslation, out modelInvers);
            Matrix3X3<float> normalMatrix = new Matrix3X3<float>(Matrix4X4.Transpose(modelInvers));

            Gl.UniformMatrix3(location, 1, false, (float*)&normalMatrix);
            CheckError();
        }

        private static unsafe void SetMatrix(Matrix4X4<float> mx, string uniformName)
        {
            int location = Gl.GetUniformLocation(program, uniformName);
            if (location == -1)
            {
                throw new Exception($"{uniformName} uniform not found on shader.");
            }

            Gl.UniformMatrix4(location, 1, false, (float*)&mx);
            CheckError();
        }
        public static void CheckError()
        {
            var error = (ErrorCode)Gl.GetError();
            if (error != ErrorCode.NoError)
                throw new Exception("GL.GetError() returned " + error.ToString());
        }

        private static string GetEmbeddedResourceAsString(string resourceRelativePath)
        {
            string resourceFullPath = Assembly.GetExecutingAssembly().GetName().Name + "." + resourceRelativePath;

            using (var resStream = Assembly.GetExecutingAssembly().GetManifestResourceStream(resourceFullPath))
            using (var resStreamReader = new StreamReader(resStream))
            {
                var text = resStreamReader.ReadToEnd();
                return text;
            }
        }

        private static void Keyboard_KeyDown(IKeyboard keyboard, Key key, int arg3)
        {
            switch (key)
            {
                case Key.Left:
                    camera.DecreaseZYAngle();
                    break;
                case Key.Right:
                    camera.IncreaseZYAngle();
                    break;
                case Key.Down:
                    camera.IncreaseDistance();
                    break;
                case Key.Up:
                    camera.DecreaseDistance();
                    break;
                case Key.U:
                    camera.IncreaseZXAngle();
                    break;
                case Key.F:
                    camera.DecreaseZXAngle();
                    break;
                case Key.Space:
                    cubeArrangementModel.AnimationEnabled = !cubeArrangementModel.AnimationEnabled;
                    break;
                    case Key.W:
                    animalPosition.Z -= 1f;
                    break;
                case Key.S:
                    animalPosition.Z += 1f;
                    break;
                case Key.A:
                    animalPosition.X -= 1f;
                    break;
                case Key.D:
                    animalPosition.X += 1f;
                    break;

            }
        }
    }
}
