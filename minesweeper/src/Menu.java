/*
    Description
    - Responsible for displaying the start menu of the game
    and offering the option of displaying the game description for the user
    - The size of the board and the number of mines can be modified here
 */



import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Menu {
    private JFrame frame;

    public Menu() {
        frame = new JFrame("Game Menu");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300, 100);
        frame.setLocationRelativeTo(null);
        frame.setResizable(false);
        frame.setLayout(new BorderLayout());

        JPanel panel = new JPanel();
        panel.setLayout(new FlowLayout());

        JButton startButton = new JButton("Start Game");
        startButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                frame.dispose();
                new Controller(8, 8, 10);
            }
        });

        JButton instructionButton = new JButton("Instructions");
        instructionButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                displayInstructions();
            }
        });

        panel.add(startButton);
        panel.add(instructionButton);
        frame.add(panel, BorderLayout.CENTER);
        frame.setVisible(true);
    }

    private void displayInstructions() {
        JOptionPane.showMessageDialog(frame,
                "Welcome to Minesweeper!\n\nInstructions:\n1. Clear all non-mine cells to win.\n2. Right-click to flag " +
                        "a cell as a mine.\n3. Left-click to reveal a cell.\n4. Avoid clicking on mines.\n5. To exit the " +
                        "game close the window.\n\nGood luck!",
                "Game Instructions",
                JOptionPane.INFORMATION_MESSAGE);
    }
}
