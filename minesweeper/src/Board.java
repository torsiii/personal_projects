/*
    Description
    - Responsible for initialising the game board, and managing its data
    - Gives access to the Controller to interact with the game board's data
    - Cell[][] cells -> represents the game board
    - ArrayList<Cell> mines -> list of cells that contain mines
 */



import java.util.ArrayList;
import java.util.Random;
import java.util.stream.IntStream;

public class Board {
    private final int numRows;
    private final int numCols;
    private final int numMines;
    private final Cell[][] cells;
    private final ArrayList<Cell> mines;
    private final Random random;

    public Board(int numRows, int numCols, int numMines) {
        this.numRows = numRows;
        this.numCols = numCols;
        this.numMines = numMines;
        this.cells = new Cell[numRows][numCols];
        this.mines = new ArrayList<>();
        this.random = new Random();

        boardInit();
    }

    public Cell[][] getCells() {
        return cells;
    }

    public ArrayList<Cell> getMines() {
        return mines;
    }

    public boolean isMine(Cell cell) {
        return mines.stream().anyMatch(mine -> mine.equals(cell));
    }

    private void boardInit() {
        IntStream.range(0, numRows).forEach(i ->
                IntStream.range(0, numCols).forEach(j -> cells[i][j] = new Cell(i, j))
        );

        int minesToBePlaced = numMines;

        while (minesToBePlaced > 0) {
            int currentRow = random.nextInt(numRows), currentCol = random.nextInt(numCols);
            Cell cell = cells[currentRow][currentCol];

            if (!mines.contains(cell)) { //preventing duplicate mines
                mines.add(cell);
                minesToBePlaced--;
            }
        }
    }
}
