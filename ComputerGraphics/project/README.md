# 3D Game

A small 3D game developed in **C#** using **Silk.NET** and **OpenGL** as the final project for a **Computer Graphics** course.

The game places the player into a textured 3D environment surrounded by a skybox. The objective is to explore the map, avoid moving enemies, and collect all red fields before getting caught.

---

## Features

- 3D world rendered with OpenGL
- Skybox-based environment
- Textured ground and player model
- OBJ model loading with normals and texture coordinates
- Phong lighting and shading
- Free camera and player-following camera
- Keyboard-controlled player movement
- Animated enemy movement
- Collision detection
- Collectible objectives
- Win and lose conditions
- ImGui in-game interface

---

## Gameplay

The player controls a cat that can freely move around the world.

Three enemy objects continuously patrol the map. Touching any enemy immediately ends the game.

Several red fields are randomly placed throughout the environment. The goal is to collect every red field while avoiding the enemies.

The game is won once every collectible has been gathered.

---

## Controls

| Key                  | Action                                                 |
| -------------------- | ------------------------------------------------------ |
| **W**                | Move forward                                           |
| **A**                | Move left                                              |
| **S**                | Move backward                                          |
| **D**                | Move right                                             |
| **Arrow Keys**       | Rotate and zoom the camera                             |
| **U / F**            | Adjust camera angle                                    |
| **Space**            | Toggle animation                                       |
| **Cat View (ImGui)** | Switch between free camera and player-following camera |

---

## Graphics Techniques

The project demonstrates several fundamental computer graphics concepts:

- OpenGL rendering pipeline
- Vertex and fragment shaders
- Perspective projection
- Model, View and Projection (MVP) matrices
- Normal matrix calculation
- Diffuse and specular lighting
- Texture mapping
- Skybox rendering
- OBJ model loading
- Vertex normals
- Camera transformations
- Real-time rendering

---

## Game Mechanics

### Player

- Keyboard-controlled movement
- Textured 3D model
- Collision detection with enemies
- Collection of objectives

### Enemies

- Automatically move back and forth
- Cause an immediate game over upon collision

### Collectibles

- Spawn at random locations
- Removed after collection
- Counter displayed through the ImGui interface

---

## Technologies

- C#
- .NET
- Silk.NET
- OpenGL
- ImGui.NET
- StbImageSharp

---

## Project Structure

```text
Program.cs                     Main application and game loop
ModelObjectDescriptor.cs       Model loading and rendering
CubeArrangementModel.cs        Animation management
ObjVertexTransformationData.cs Vertex normal calculations
Shaders/                       Vertex and fragment shaders
Resources/                     OBJ models and textures
```

---

## Author

Developed as the final project for the **Computer Graphics** course, demonstrating the implementation of a small interactive 3D game using **Silk.NET** and **OpenGL**.
