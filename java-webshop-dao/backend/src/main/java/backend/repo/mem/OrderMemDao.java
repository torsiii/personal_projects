package backend.repo.mem;

import backend.exception.DataAccessException;
import backend.model.Order;
import backend.repo.OrderDao;

import java.util.Collection;
import java.util.stream.Collectors;

public class OrderMemDao extends MemDao<Order> implements OrderDao {

    @Override
    public Collection<Order> findByOrderDate(String date) throws DataAccessException {
        if (date == null || date.isBlank()) {
            throw new DataAccessException("date must not be empty");
        }
        return entities.values().stream()
                .filter(o -> date.equals(o.getOrderDate()))
                .collect(Collectors.toList());
    }

    @Override
    public Order findByDeliveryAddress(String address) throws DataAccessException {
        if (address == null || address.isBlank()) {
            throw new DataAccessException("address must not be empty");
        }
        return entities.values().stream()
                .filter(o -> address.equals(o.getDeliveryAddress()))
                .findFirst()
                .orElse(null);
    }

    @Override
    public Order findById(String id) throws DataAccessException {
        try {
            long longId = Long.parseLong(id.trim());
            return entities.get(longId);
        } catch (NumberFormatException e) {
            throw new DataAccessException("Invalid id: " + id);
        }
    }
}
