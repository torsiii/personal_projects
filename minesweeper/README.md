# Minesweeper Game - Java Swing Implementation

## Overview
This project is a Minesweeper game implemented in Java using Swing for the graphical user interface. The game follows the classic Minesweeper rules, where the player must reveal all non-mine cells to win while avoiding stepping mines. The game features a GUI, sound effects, and a timer, making it an engaging and interactive experience.

## Features
- Graphical User Interface (GUI) using Java Swing.
- Customizable board size and mine count.
- Left-click to reveal a cell.
- Right-click to place or remove a flag.
- Automatic revealing of empty neighboring cells.
- Game status updates (win/loss messages).
- Timer to track playtime.
- Background music and sound effects for different events (game start, victory, loss).
- Screenshot saving option upon game completion.

## How to Play
- **Left-click** on a cell to reveal its content:
  - If it contains a mine, the game is over.
  - If it is empty and has no neighboring mines, the game will automatically reveal nearby empty cells.
  - If it has neighboring mines, the number of adjacent mines is displayed.
  
- **Right-click** to mark a cell as a potential mine (flagging).

The game ends when:
- All non-mine cells are revealed (win).
- A mine is clicked (loss).

If the game is won, the player can save a screenshot of the board.
