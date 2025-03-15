/*
    Description
    - The Cell class represents an individual cell in the Minesweeper game grid
    - Provides the unit for interacting with the game board
    - Each instance holds its row and column indice from the board to allow the controller to find its position and preform operations with the cell
    - Represents a "bridge" between the visual(Game class) and the logical(Board class) representation
 */


import javax.swing.*;
import java.awt.*;

public class Cell extends JButton {
    private int row;
    private int col;

    public Cell(int row, int col) {
        this.row = row;
        this.col = col;
        setFont(new Font("Arial", Font.BOLD, 45));
    }

    public int getRow() {
        return row;
    }

    public int getCol() {
        return col;
    }
}
