package desktop.presentation;

import backend.exception.ServiceException;
import backend.model.Order;
import backend.service.WebShop;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

public class OrderUi extends JFrame {
    private final transient WebShop webShop;
    private final DefaultListModel<Order> listModel;
    private final JList<Order> list;

    private final JTextField orderDateField = new JTextField();
    private final JTextField deliveryAddressField = new JTextField();
    private final JTextField sumField = new JTextField();
    private final JCheckBox stateBox = new JCheckBox();
    private final JTextField itemNumberField = new JTextField();

    public OrderUi(WebShop webShop) {
        super();
        this.webShop = webShop;
        listModel = new DefaultListModel<>();
        list = new JList<>(listModel);

        setTitle("WebShop");
        setSize(700, 400);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout(12, 12));

        list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        list.setCellRenderer((lst, value, index, isSelected, cellHasFocus) -> {
            JLabel lbl = new JLabel(render(value));
            if (isSelected) {
                lbl.setOpaque(true);
            }
            lbl.setBorder(BorderFactory.createEmptyBorder(4, 6, 4, 6));
            return lbl;
        });

        list.addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                Order o = list.getSelectedValue();
                if (o != null) {
                    fillForm(o);
                }
            }
        });

        JPanel listPanel = new JPanel(new BorderLayout(6, 6));
        listPanel.add(new JLabel("list of orders:"), BorderLayout.NORTH);
        listPanel.add(new JScrollPane(list), BorderLayout.CENTER);
        add(listPanel, BorderLayout.CENTER);

        JPanel formPanel = new JPanel(new GridLayout(5, 2, 8, 8));
        formPanel.add(new JLabel("orderDate:"));
        formPanel.add(orderDateField);
        formPanel.add(new JLabel("deliveryAddress"));
        formPanel.add(deliveryAddressField);
        formPanel.add(new JLabel("sum"));
        formPanel.add(sumField);
        formPanel.add(new JLabel("state"));
        formPanel.add(stateBox);
        formPanel.add(new JLabel("number of items"));
        formPanel.add(itemNumberField);

        JButton addBtn = new JButton(new AbstractAction("Add") {
            @Override
            public void actionPerformed(ActionEvent e) {
                onAdd();
            }
        });
        JButton updateBtn = new JButton(new AbstractAction("Update") {
            @Override
            public void actionPerformed(ActionEvent e) {
                onUpdate();
            }
        });
        JButton deleteBtn = new JButton(new AbstractAction("Delete") {
            @Override
            public void actionPerformed(ActionEvent e) {
                onDelete();
            }
        });


        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttons.add(addBtn);
        buttons.add(updateBtn);
        buttons.add(deleteBtn);

        JPanel right = new JPanel(new BorderLayout(6, 6));
        right.add(new JLabel("Details:"), BorderLayout.NORTH);
        right.add(formPanel, BorderLayout.CENTER);
        right.add(buttons, BorderLayout.SOUTH);

        add(right, BorderLayout.EAST);
    }

    private static String render(Order o) {
        return String.format("#%d | %s | %s | sum=%.2f | state=%s | items=%d",
                o.getId(),
                o.getOrderDate(),
                o.getDeliveryAddress(),
                o.getSum(),
                o.isState(),
                o.getItemNumber());
    }

    private void fillForm(Order o) {
        orderDateField.setText(o.getOrderDate());
        deliveryAddressField.setText(o.getDeliveryAddress());
        sumField.setText(Double.toString(o.getSum()));
        stateBox.setSelected(o.isState());
        itemNumberField.setText(Integer.toString(o.getItemNumber()));
    }

    private Order readFromForm() {
        String orderDate = orderDateField.getText().trim();
        String deliveryAddress = deliveryAddressField.getText().trim();

        double sum;
        try {
            sum = Double.parseDouble(sumField.getText().trim());
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this,
                    "sum is not a number", "Validation", JOptionPane.WARNING_MESSAGE);
            return null;
        }

        int itemNumber;
        try {
            itemNumber = Integer.parseInt(itemNumberField.getText().trim());
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this,
                    "itemNumber is not a number", "Validation", JOptionPane.WARNING_MESSAGE);
            return null;
        }

        boolean state = stateBox.isSelected();
        return new Order(orderDate, deliveryAddress, sum, state, itemNumber);
    }

    private void onAdd() {
        try {
            Order newOrder = readFromForm();
            if (newOrder == null) {
                return;
            }
            webShop.placeOrder(newOrder);
            loadOrders();
            JOptionPane.showMessageDialog(this, "Added.");
        } catch (ServiceException ex) {
            JOptionPane.showMessageDialog(this, "Add failed: " + ex.getInfo(), "Error", JOptionPane.ERROR_MESSAGE);
        } 
    }

    private void onUpdate() {
        Order selected = list.getSelectedValue();
        if (selected == null) {
            JOptionPane.showMessageDialog(this, "Choose an order to update");
            return;
        }
        try {
            Order edited = readFromForm();
            if (edited == null) {
                return;
            }
            webShop.updateOrder(selected.getId(), edited);
            loadOrders();
            JOptionPane.showMessageDialog(this, "Updated.");
        } catch (ServiceException ex) {
            JOptionPane.showMessageDialog(this, "Update failed: " + ex.getInfo(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void onDelete() {
        Order selected = list.getSelectedValue();
        if (selected == null) {
            JOptionPane.showMessageDialog(this, "Choose an order to delete");
            return;
        }

        int ok = JOptionPane.showConfirmDialog(this,
                "Do you want to delete (#" + selected.getId() + ")?",
                "Confirm delete", JOptionPane.YES_NO_OPTION);
        if (ok != JOptionPane.YES_OPTION) {
            return;
        }

        try {
            webShop.deleteOrder(selected.getId());
            loadOrders();
            JOptionPane.showMessageDialog(this, "Deleted.");
        } catch (ServiceException ex) {
            JOptionPane.showMessageDialog(this, "Delete failed: " + ex.getInfo(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void loadOrders() {
        listModel.clear();
        try {
            for (Order line : webShop.listOrders()) {
                listModel.addElement(line);
            }
        } catch (ServiceException e) {
            JOptionPane.showMessageDialog(this, "Load failed: " + e.getInfo(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    public void loadInitialData() {
        loadOrders();
    }
}

