import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.ArrayList;
import java.util.Random;
import javax.swing.Timer;
import java.awt.Point;
import java.util.List;

public class GamePanel extends JPanel implements KeyListener {
    private JSlider angleSlider;
    private JSlider velocitySlider;
    private JButton jButton;
    private JLabel angleLabel;
    private JLabel velocityLabel;

    private final int groundY = 400;
    private final int catapultWidth = 50;
    private int catapultX = 70;
    private int targetX;
    private final int targetSize = 20;
    private final Random random = new Random();
    private boolean isPlaced = false;
    private boolean isShooting = false;
    private double posX, posY;
    private double velX, velY;
    private final double dt = 0.05; //mp
    private Timer timer;
    private final List<Point> pathPoints = new ArrayList<>();

    public GamePanel() {
        angleSlider = new JSlider(10, 80, 45);
        velocitySlider = new JSlider(10, 100, 50);
        jButton = new JButton("shoot");
        angleLabel = new JLabel("angle: 45");
        velocityLabel = new JLabel("speed: 50");

        angleSlider.addChangeListener(e -> {
            angleLabel.setText("angle: " + angleSlider.getValue());
            requestFocusInWindow();
        });
        velocitySlider.addChangeListener(e -> {
            velocityLabel.setText("speed: " + velocitySlider.getValue());
            requestFocusInWindow();
        });
        jButton.addActionListener(e -> startShoot());

        add(angleSlider);
        add(velocitySlider);
        add(jButton);
        add(angleLabel);
        add(velocityLabel);

        setBackground(Color.PINK);
        addKeyListener(this);
        setFocusable(true);
        requestFocusInWindow();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        g.setColor(Color.black);
        g.drawLine(0, groundY, getWidth(), groundY);
        g.setColor(Color.blue);
        g.fillRect(catapultX, groundY - 30, catapultWidth, 30);

        if (!isPlaced) {
            targetX = 534 + random.nextInt(246);
            isPlaced = true;
        }

        g.setColor(Color.red);
        g.fillOval(targetX, groundY - targetSize, targetSize, targetSize);

        if (isShooting) {
            g.setColor(Color.MAGENTA);
            g.fillOval((int) posX, (int) posY, 10, 10);
        }

        g.setColor(Color.gray);
        for(Point p : pathPoints){
            g.fillRect(p.x, p.y, 2, 2);
        }

    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();
        if (key == KeyEvent.VK_LEFT && catapultX > 0) {
            catapultX -= 10;
        }

        if (key == KeyEvent.VK_RIGHT && catapultX < 266 - catapultWidth) {
            catapultX += 10;
        }

        repaint();
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }

    private void startShoot() {
        if (isShooting) return;

        isShooting = true;
        angleSlider.setEnabled(false);
        velocitySlider.setEnabled(false);
        jButton.setEnabled(false);

        double angle = Math.toRadians(angleSlider.getValue());
        double velocity = velocitySlider.getValue();

        posX = catapultX + catapultWidth;
        posY = groundY - 30;

        velX = velocity * Math.cos(angle);
        velY = -velocity * Math.sin(angle);

        requestFocusInWindow();

        timer = new Timer((int) (dt * 1000), e -> update());
        timer.start();
    }

    private void update() {
        posX += velX * dt;
        posY += velY * dt;
        velY += 9.8 * dt;

        pathPoints.add(new Point((int) posX, (int) posY));
        repaint();

        if (posY >= groundY) {
            timer.stop();
            isShooting = false;
            check();
        }
    }

    private void check() {
        if (Math.abs(posX - targetX) < targetSize) {
            JOptionPane.showMessageDialog(this, "You hit the target! :D");
            System.exit(0);
        } else {
            JOptionPane.showMessageDialog(this, "Target missed! :(");
            pathPoints.clear();
            repaint();

            isShooting=false;
            angleSlider.setEnabled(true);
            velocitySlider.setEnabled(true);
            jButton.setEnabled(true);
        }
    }
}
