/*
    Description
    - Responsible for managing the user interface of the game
    - window -> main window of the game
    - textLabel -> displays the timer
    - boardPanel -> holds the cells of the game
 */


import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Game {
    private final JFrame window;
    private final JLabel textLabel;
    private final JPanel boardPanel;
    private int currentTimerValue;
    private Timer timer;

    public Game(int width, int hieght, int numRows, int numCols) {
        window = new JFrame("Minesweeper");
        textLabel = new JLabel();
        boardPanel = new JPanel();

        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        window.setSize(width, hieght);
        window.setLocationRelativeTo(null);
        window.setResizable(false);
        window.setLayout(new BorderLayout());

        textLabel.setFont(new Font("Arial", Font.BOLD, 30));
        textLabel.setHorizontalAlignment(JLabel.CENTER);

        window.add(textLabel, BorderLayout.NORTH);

        boardPanel.setLayout(new GridLayout(numRows, numCols));
        window.add(boardPanel, BorderLayout.CENTER);

        timer = new Timer(1000, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                currentTimerValue++;
                textLabel.setText(Integer.toString(currentTimerValue));
            }
        });
        timer.start();

        window.setVisible(true);
    }

    public JLabel getTextLabel() {
        return textLabel;
    }

    public JPanel getBoardPanel() {
        return boardPanel;
    }

    public int getCurrentTimerValue() {
        return this.currentTimerValue;
    }

    public Timer getTimer() {
        return timer;
    }

    public JFrame getWindow() {
        return window;
    }
}
