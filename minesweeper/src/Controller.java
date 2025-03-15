/*
    Description
    - Responsible for handling the core game logic
    - Responds to user actions, and interacts with the board and game UI
 */



import javax.imageio.ImageIO;
import javax.sound.sampled.*;
import javax.swing.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Controller {
    private final Game game;
    private final Board board;
    private int cellsRevealed;
    private boolean gameOver;
    private Clip clip;

    private ImageIcon scaleImageIcon(ImageIcon icon, int width, int height) {
        return new ImageIcon(icon.getImage().getScaledInstance(width, height, java.awt.Image.SCALE_SMOOTH));
    }

    private final ImageIcon bombIcon = scaleImageIcon(new ImageIcon("src/minesweeper/res/bomb.png"), 80, 55);
    private final ImageIcon flagIcon = scaleImageIcon(new ImageIcon("src/minesweeper/res/flag.png"), 65, 65);


    public Controller(int numRows, int numCols, int numMines) {
        try { //background music
            AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File("C:\\Users\\totho\\OneDrive\\Documents\\javaLabor\\projekt\\pirates.wav"));
            clip = AudioSystem.getClip();
            clip.open(audioInputStream);
            clip.loop(Clip.LOOP_CONTINUOUSLY);
        } catch (UnsupportedAudioFileException | LineUnavailableException | IOException e) {
            System.out.println("IO error");
        }

        game = new Game(numCols * 65, numRows * 65, numRows, numCols);
        board = new Board(numRows, numCols, numMines);

        Cell[][] cells = board.getCells();
        JPanel boardPanel = game.getBoardPanel();

        for (Cell[] currentRow : cells) {
            for (Cell currentCell : currentRow) {
                currentCell.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mousePressed(MouseEvent e) {
                        if (gameOver) {
                            return;
                        }

                        if (e.getButton() == MouseEvent.BUTTON1) {
                            handleLeftClick(currentCell);
                        } else if (e.getButton() == MouseEvent.BUTTON3) {
                            handleRightClick(currentCell);
                        }
                    }
                });
                boardPanel.add(currentCell);
            }
        }
        game.getTextLabel().setText("Minesweeper start");
    }

    private void handleLeftClick(Cell cell) {
        //- reveals the content of the cell
        //- if it was a mine => all mines should be revealed and the game is over
        //  |-> otherwise: if the neighbouring cells contain mines the number is displayed in the cell, if not the neighbours are revealed
        //- if all non-mine cells are revealed the game is won and the user is offered the option to save a screenshot of the game
        if (!cell.isEnabled()) {
            return;
        }

        if (board.isMine(cell)) {
            for (Cell c : board.getMines()) {
                c.setIcon(bombIcon);
            }
            clip.stop();
            game.getTimer().stop();
            game.getTextLabel().setText("Game Over! time spent: " + game.getCurrentTimerValue() + " sec.");
            gameOver = true;
            try { //losing sound effect
                AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File("fail.wav"));
                clip = AudioSystem.getClip();
                clip.open(audioInputStream);
                clip.start();
            } catch (UnsupportedAudioFileException | LineUnavailableException | IOException e) {
                System.out.println("IO error");
            }
        } else {
            cell.setEnabled(false);
            cellsRevealed++;

            int minesFound = countNeighbours(cell.getRow(), cell.getCol());
            if (minesFound > 0) {
                cell.setText(String.valueOf(minesFound));
            } else {
                revealNeighbours(cell.getRow(), cell.getCol());
            }

            if (cellsRevealed == board.getCells().length * board.getCells()[0].length - board.getMines().size()) {
                clip.stop();
                game.getTimer().stop();
                game.getTextLabel().setText("All mines cleared! time spent: " + game.getCurrentTimerValue() + " sec.");
                gameOver = true;

                try { //victory sound effect
                    AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File("victory.wav"));
                    clip = AudioSystem.getClip();
                    clip.open(audioInputStream);
                    clip.start();
                } catch (UnsupportedAudioFileException | LineUnavailableException | IOException e) {
                    System.out.println("IO error");
                }

                takeScreenshot(game.getWindow());
            }
        }
    }

    private void handleRightClick(Cell cell) {
        if (!cell.isEnabled()) {
            return;
        }

        if (cell.getIcon() == null) {
            cell.setIcon(flagIcon);
        } else if (cell.getIcon() == flagIcon) {
            cell.setIcon(null);
        }
    }

    private int countNeighbours(int row, int col) {
        int counter = 0;
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                int newRow = row + i;
                int newCol = col + j;
                if (i == 0 && j == 0) {
                    continue;
                }
                if (newRow >= 0 && newRow < board.getCells().length && newCol >= 0 && newCol < board.getCells()[0].length) {
                    if (board.isMine(board.getCells()[newRow][newCol])) {
                        counter++;
                    }
                }
            }
        }
        return counter;
    }

    private void revealNeighbours(int row, int col) {
        //recursively reveals neighbouring cells that are not mines and are not surrounded by them
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                int newRow = row + i;
                int newCol = col + j;
                if (newRow >= 0 && newRow < board.getCells().length && newCol >= 0 && newCol < board.getCells()[0].length) {
                    Cell neighbor = board.getCells()[newRow][newCol];
                    if (!neighbor.isEnabled()) {
                        continue;
                    }
                    neighbor.setEnabled(false);
                    cellsRevealed++;

                    int minesFound = countNeighbours(newRow, newCol);
                    if (minesFound > 0) {
                        neighbor.setText(String.valueOf(minesFound));
                    } else {
                        revealNeighbours(newRow, newCol);
                    }
                }
            }
        }
    }

    private void takeScreenshot(JFrame frame) {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Save Screenshot of Completed Game");
        int userSelection = fileChooser.showSaveDialog(null);

        if (userSelection == JFileChooser.APPROVE_OPTION) {
            File fileToSave = fileChooser.getSelectedFile();
            try {
                BufferedImage image = new BufferedImage(frame.getWidth(), frame.getHeight(), BufferedImage.TYPE_INT_RGB);
                frame.paint(image.getGraphics());
                ImageIO.write(image, "png", new File(fileToSave.getAbsolutePath() + ".png"));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
