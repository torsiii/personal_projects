import  javax.swing.*;

public class GameView {
    public static void main(String[] args) {
        JFrame jFrame = new JFrame("Catapult game");
        jFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        jFrame.setResizable(false);
        jFrame.setSize(800, 500);
        jFrame.setLocationRelativeTo(null);

        GamePanel gamePanel = new GamePanel();
        jFrame.add(gamePanel);
        jFrame.setVisible(true);
    }
}
