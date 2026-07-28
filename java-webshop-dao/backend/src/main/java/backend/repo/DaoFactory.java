package backend.repo;

import backend.config.ConfigManager;
import backend.config.DaoType;
import backend.repo.jdbc.JdbcDaoFactory;
import backend.repo.mem.MemDaoFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public abstract class DaoFactory {

    private static final Logger LOG = LoggerFactory.getLogger(DaoFactory.class);
    private static DaoFactory instance;

    public static synchronized DaoFactory getInstance() {
        if (instance == null) {
            DaoType daoType = ConfigManager.getConfig().getDaoType();

            LOG.info("Initializing DaoFactory with type: {}", daoType);

            if (daoType == DaoType.JDBC) {
                instance = new JdbcDaoFactory();
            } else if (daoType == DaoType.MEMORY) {
                instance = new MemDaoFactory();
            } else {
                throw new IllegalStateException("Unsupported DAO type: " + daoType);
            }
        }

        return instance;
    }

    public abstract OrderDao getOrderDao();
}