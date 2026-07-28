package backend.repo.jdbc;

import backend.exception.DataAccessException;
import backend.model.Order;
import backend.repo.OrderDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.*;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class OrderJdbcDao implements OrderDao {
    private static final Logger LOG = LoggerFactory.getLogger(OrderJdbcDao.class);

    @Override
    public void create(Order entity) throws DataAccessException {
        String sql = "INSERT INTO orders(order_date, delivery_address, sum, state, item_number) "
                + "VALUES (?, ?, ?, ?, ?)";

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, entity.getOrderDate());
            ps.setString(2, entity.getDeliveryAddress());
            ps.setDouble(3, entity.getSum());
            ps.setBoolean(4, entity.isState());
            ps.setInt(5, entity.getItemNumber());

            int rows = ps.executeUpdate();

            LOG.info("Inserted component rows={}, date='{}', address='{}'",
                    rows, entity.getOrderDate(), entity.getDeliveryAddress());

            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    entity.setId(rs.getLong(1));
                }
            }

        } catch (SQLException e) {
            LOG.error("Error inserting component into database: date='{}', address='{}', message={}",
                    entity.getOrderDate(), entity.getDeliveryAddress(), e.getMessage(), e);
            throw new DataAccessException("Create failed: " + e.getMessage());
        }
    }

    @Override
    public void update(String id, Order entity) throws DataAccessException {
        String sql = "UPDATE orders "
                + "SET order_date = ?, delivery_address = ?, sum = ?, state = ?, item_number = ? "
                + "WHERE id = ?";

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            long longId = Long.parseLong(id.trim());

            ps.setString(1, entity.getOrderDate());
            ps.setString(2, entity.getDeliveryAddress());
            ps.setDouble(3, entity.getSum());
            ps.setBoolean(4, entity.isState());
            ps.setInt(5, entity.getItemNumber());
            ps.setLong(6, longId);

            int n = ps.executeUpdate();
            if (n == 0) {
                LOG.warn("update: id not found (id={})", id);
                throw new DataAccessException("Entity not found with id=" + id);
            }

            entity.setId(longId);
            LOG.info("Updated order id={}", id);

        } catch (SQLException | NumberFormatException e) {
            LOG.error("Error updating order id={}: {}", id, e.getMessage(), e);
            throw new DataAccessException("Update failed: " + e.getMessage());
        }
    }

    @Override
    public void delete(String id) throws DataAccessException {
        String sql = "DELETE FROM orders WHERE id = ?";

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            long longId = Long.parseLong(id.trim());
            ps.setLong(1, longId);

            int n = ps.executeUpdate();
            if (n == 0) {
                LOG.warn("delete: id not found (id={})", id);
                throw new DataAccessException("Entity not found with id=" + id);
            }

            LOG.info("Deleted order id={}", id);
        } catch (SQLException | NumberFormatException e) {
            LOG.error("delete failed id={}", id, e);
            throw new DataAccessException("Delete failed: " + e.getMessage());
        }
    }

    @Override
    public List<Order> read() throws DataAccessException {
        String sql = "SELECT id, order_date, delivery_address, sum, state, item_number FROM orders";
        List<Order> result = new ArrayList<>();

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                result.add(map(rs));
            }

            LOG.info("Read orders count={}", result.size());
            return result;
        } catch (SQLException e) {
            LOG.error("read failed (sqlState={}, code={})", e.getSQLState(), e.getErrorCode(), e);
            throw new DataAccessException("Read failed: " + e.getMessage());
        }
    }

    @Override
    public Collection<Order> findByOrderDate(String date) throws DataAccessException {
        if (date == null || date.isBlank()) {
            throw new DataAccessException("date must not be empty");
        }

        String sql = "SELECT id, order_date, delivery_address, sum, state, item_number "
                + "FROM orders WHERE order_date = ?";

        List<Order> result = new ArrayList<>();

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, date);

            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    result.add(map(rs));
                }
            }

            LOG.info("returning orders with date={}", date);
            return result;
        } catch (SQLException e) {
            LOG.error("No orders found with date={}", date, e);
            throw new DataAccessException("Find by order date failed: " + e.getMessage());
        }
    }

    @Override
    public Order findByDeliveryAddress(String address) throws DataAccessException {
        if (address == null || address.isBlank()) {
            throw new DataAccessException("address must not be empty");
        }

        String sql = "SELECT id, order_date, delivery_address, sum, state, item_number "
                + "FROM orders WHERE delivery_address = ? LIMIT 1";

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, address);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    LOG.info("returning orders with adress={}", address);
                    return map(rs);
                }
                return null;
            }


        } catch (SQLException e) {
            LOG.error("Find by delivery address={} failed:", address, e);
            throw new DataAccessException("Find by delivery address failed: " + e.getMessage());
        }
    }

    private Order map(ResultSet rs) throws SQLException {
        return new Order(
                rs.getLong("id"),
                rs.getString("order_date"),
                rs.getString("delivery_address"),
                rs.getDouble("sum"),
                rs.getBoolean("state"),
                rs.getInt("item_number")
        );
    }

    @Override
    public Order findById(String id) throws DataAccessException {
        String sql = "SELECT id, order_date, delivery_address, sum, state, item_number "
                + "FROM orders WHERE id = ?";

        try (Connection conn = JdbcConnectionFactory.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            long longId = Long.parseLong(id.trim());
            ps.setLong(1, longId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return map(rs);
                }
                return null;
            }
        } catch (SQLException | NumberFormatException e) {
            throw new DataAccessException("Find by id failed: " + e.getMessage());
        }
    }
}