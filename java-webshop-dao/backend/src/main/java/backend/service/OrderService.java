package backend.service;

import backend.exception.ServiceException;
import backend.model.Order;

import java.util.List;

public interface OrderService {
    void placeOrder(Order order) throws ServiceException;

    List<Order> listOrders() throws ServiceException;

    void updateOrder(Long id, Order edited) throws ServiceException;

    void deleteOrder(Long id) throws ServiceException;

    Order getOrderById(Long id) throws ServiceException;
}
