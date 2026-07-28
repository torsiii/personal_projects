package spring.service;

import spring.exception.ServiceException;
import spring.model.Order;

import java.util.List;

public interface OrderService {
    void placeOrder(Order order) throws ServiceException;

    List<Order> listOrders() throws ServiceException;

    void updateOrder(Long id, Order edited) throws ServiceException;

    void deleteOrder(Long id) throws ServiceException;

    Order getOrderById(Long id) throws ServiceException;

    List<Order> getOrdersByDate(String orderDate) throws ServiceException;
}
