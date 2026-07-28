package desktop;

import desktop.presentation.OrderUi;
import backend.repo.DaoFactory;
import backend.service.WebShop;

import javax.swing.*;

public class Main {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            var dao = DaoFactory.getInstance().getOrderDao();

            WebShop webShop = new WebShop(dao);
            OrderUi orderUi = new OrderUi(webShop);

            orderUi.loadInitialData();
            orderUi.setVisible(true);
            orderUi.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        });
    }
}
