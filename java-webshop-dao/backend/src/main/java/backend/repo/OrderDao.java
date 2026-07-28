package backend.repo;

import backend.exception.DataAccessException;
import backend.model.Order;

import java.util.Collection;


public interface OrderDao extends Dao<Order> {

    Collection<Order> findByOrderDate(String date) throws DataAccessException;

    Order findByDeliveryAddress(String address) throws DataAccessException;

    @Override
    Order findById(String id) throws DataAccessException;
}
