package backend.repo.jdbc;

import backend.repo.DaoFactory;
import backend.repo.OrderDao;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JdbcDaoFactory extends DaoFactory {

    private static final Logger LOG = LoggerFactory.getLogger(JdbcDaoFactory.class);

    private static final OrderDao ORDER_DAO = createDao();

    private static OrderDao createDao() {
        LOG.info("Creating OrderJdbcDao singleton");
        return new OrderJdbcDao();
    }

    @Override
    public OrderDao getOrderDao() {
        LOG.debug("Returning OrderJdbcDao singleton");
        return ORDER_DAO;
    }
}