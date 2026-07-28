# Catapult Game

## Overview

Catapult Game is a simple Java Swing application that simulates a projectile-launching game. The player controls a movable catapult, adjusts the launch angle and velocity, and attempts to hit a randomly placed target using realistic projectile motion.

The project demonstrates the use of Java Swing for GUI development, event-driven programming, timers, keyboard input, and basic physics simulation.

## Features

- Adjustable launch angle using a slider
- Adjustable launch velocity using a slider
- Movable catapult controlled with the keyboard
- Random target generation
- Projectile trajectory visualization
- Physics-based projectile motion using gravity
- Hit and miss detection
- Simple graphical user interface

## Technologies

- Java
- Java Swing
- AWT Graphics
- Swing Timer

## Controls

| Action              | Control          |
| ------------------- | ---------------- |
| Move catapult left  | Left Arrow       |
| Move catapult right | Right Arrow      |
| Adjust launch angle | Angle slider     |
| Adjust launch speed | Speed slider     |
| Fire projectile     | **Shoot** button |

## Game Rules

1. Move the catapult to the desired position using the arrow keys.
2. Adjust the launch angle.
3. Adjust the launch speed.
4. Press **Shoot** to launch the projectile.
5. If the projectile hits the target, you win.
6. If you miss, the trajectory is cleared and you can try again.

## Physics

The projectile follows a basic ballistic trajectory.

The initial velocity components are calculated as:

```text
vx = v × cos(angle)
vy = -v × sin(angle)
```

Gravity is applied during each simulation step, resulting in a realistic projectile arc.

## Project Structure

```text
src/
├── GameView.java      // Application entry point
└── GamePanel.java     // Game logic, rendering, physics and controls
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/your-username/catapult_game.git
```

Compile the project:

```bash
javac src/*.java
```

Run the application:

```bash
java -cp src GameView
```

## Learning Objectives

This project demonstrates:

- Java Swing GUI development
- Event-driven programming
- Keyboard event handling
- Graphics rendering
- Animation using Swing Timer
- Basic projectile physics
- Object-oriented programming

## Author

Created as a Java programming project for practicing GUI development, event handling, and basic physics simulation.
