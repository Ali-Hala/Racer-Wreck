# Racer Wreck

## Overview
This Python code is a game project developed as a final assignment. The game, named "Racer Wreck," is designed as a racing game where players control a car on a track while avoiding collisions with the track walls and competing against a computer-controlled car. The game features multiple levels and includes functionalities such as collision detection, level progression, time tracking, and user interface elements.

## Instructions
1. Ensure Python and Pygame are installed on your system.
2. Run the code in a Python environment that supports Pygame.
3. Follow on-screen instructions to navigate through the start screen, rules screen, and gameplay.
4. Use keyboard controls to maneuver your car (W for forward, A for left, D for right, S for backward).
5. Complete levels by reaching the finish line while avoiding collisions with track walls and beating the computer car to the finish line.
6. On completion, you'll be presented with an end screen showing credits and options to quit or retry.

## Key Features
- **Game Levels:** The game consists of multiple levels, with each level presenting increasing challenges.
- **Player and Computer Cars:** Players control one car while competing against a computer-controlled car.
- **Collision Detection:** Collision detection is implemented to handle collisions between the player's car and the track walls.
- **Time Tracking:** The game tracks the time taken by the player to complete each level.
- **User Interface:** Start, rules, and end screens provide a user-friendly interface for navigation and interaction.

## File Structure
- `startbackground.jpg`: Image file for the start screen background.
- `Start.png`: Image file for the start button.
- `Quit.png`: Image file for the quit button.
- `How_to_play_CarGame.png`: Image file for the rules screen background.
- `Credits_CarGame.png`: Image file for the credits screen background.
- `grass.jpg`, `mountain.jpg`, `dirt.jpg`: Image files for different track backgrounds.
- `track.png`: Image file for the track layout.
- `track-border.png`: Image file for the track border used in collision detection.
- `finish.png`: Image file for the finish line.
- `grey-car.png`, `racecar.png`: Image files for player and computer cars.
- `README.md`: Readme file providing an overview of the project.
- `game.py`: Python code file containing the game implementation.

## Code Explanation

The provided Python code implements a 2D racing game using the Pygame library. Here's a breakdown of how the code works:

### Initialization and Setup
- The code initializes Pygame and sets up the game window with a defined screen size.
- Necessary libraries such as Pygame and math are imported.
- Images for various game elements like the track, cars, and backgrounds are loaded and scaled as needed.

### Classes and Objects
- **Car Class**: Defines a generic car object with attributes for position, velocity, and rotation. Subclasses include PlayerCar and ComputerCar, each with specific functionalities for player-controlled and computer-controlled cars, respectively.
- **Button Class**: Represents clickable buttons on the game interface, enabling user interaction for starting the game, quitting, or retrying levels.
- **GameControl Class**: Manages game levels, tracks level progression, and controls game start/end states.

### Game Loop and Logic
- **Main Game Loop**: The core loop handles game rendering, user input, and game state updates.
- **User Input Handling**: Keyboard input is processed to control player car movement (WASD keys) and interact with the game interface.
- **Collision Detection**: Collision detection is implemented to detect collisions between the player's car and the track boundaries.
- **Level Progression**: Players progress through multiple levels by completing each level's objectives, with increasing difficulty.
- **Time Tracking**: The game tracks the time taken by the player to complete each level, enhancing gameplay dynamics.

### Screens and Interfaces
- **Start Screen**: Provides an initial interface for starting the game, displaying game title, start button, and quit button.
- **Rules Screen**: Displays game rules and instructions to guide players on gameplay mechanics and objectives.
- **End Screen**: Appears upon completing the game, showing credits and options to quit or retry the game.

### Additional Features
- **Graphics and Visuals**: Utilizes images and graphics to enhance the game's visual appeal, including background scenery, track layout, and car models.
- **User Interface Elements**: Incorporates buttons, text, and interface elements for user interaction and feedback during gameplay.

This section provides a high-level overview of how the code is structured and functions to create the "Racer Wreck" game experience.

Thank you for playing "Racer Wreck"!
