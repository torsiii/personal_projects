package backend.service;

import backend.exception.DataAccessException;
import backend.exception.ServiceException;
import backend.model.Order;
import backend.repo.OrderDao;

import java.util.List;

public class WebShop implements OrderService {
    private final OrderDao dao;

    public WebShop(OrderDao dao) {
        this.dao = dao;
    }

    @Override
    public void placeOrder(Order order) throws ServiceException {
        try {
            dao.create(order);
        } catch (DataAccessException e) {
            throw new ServiceException("create failed: " + e.getMessage());
        }

    }

    @Override
    public List<Order> listOrders() throws ServiceException {
        try {
            return dao.read();
        } catch (DataAccessException e) {
            throw new ServiceException("error while listing orders");
        }
    }

    @Override
    public void updateOrder(Long id, Order edited) throws ServiceException {
        if (id == null) {
            throw new ServiceException("id is required");
        }
        try {
            dao.update(id.toString(), edited);
        } catch (DataAccessException e) {
            throw new ServiceException("error while updating order: " + e.getInfo());
        }
    }

    @Override
    public void deleteOrder(Long id) throws ServiceException {
        if (id == null) {
            throw new ServiceException("id is required");
        }
        try {
            dao.delete(id.toString());
        } catch (DataAccessException e) {
            throw new ServiceException("error while deleting order: " + e.getInfo());
        }
    }

    @Override
    public Order getOrderById(Long id) throws ServiceException {
        if (id == null) {
            throw new ServiceException("id is required");
        }

        try {
            return dao.findById(id.toString());
        } catch (DataAccessException e) {
            throw new ServiceException("error while reading order: " + e.getMessage());
        }
    }
}
