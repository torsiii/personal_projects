package backend.repo.jdbc;

import com.zaxxer.hikari.HikariDataSource;
import backend.config.AppConfig;
import backend.config.ConfigManager;
import backend.config.DaoType;
import backend.config.JdbcConfig;
import backend.exception.JdbcException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.SQLException;

public final class JdbcConnectionFactory {

    private static final Logger LOG = LoggerFactory.getLogger(JdbcConnectionFactory.class);
    private static final HikariDataSource DATA_SOURCE;

    static {
        try {
            AppConfig config = ConfigManager.getConfig();

            if (config.getDaoType() != DaoType.JDBC) {
                throw new JdbcException("JdbcConnectionFactory used with non-JDBC profile");
            }

            JdbcConfig jdbc = config.getJdbc();
            if (jdbc == null) {
                throw new JdbcException("Missing JDBC configuration");
            }

            // driver load
            Class.forName(jdbc.getDriverClassName());

            HikariDataSource ds = new HikariDataSource();

            ds.setJdbcUrl(jdbc.getUrl());
            ds.setUsername(jdbc.getUsername());
            ds.setPassword(jdbc.getPassword());

            ds.setMaximumPoolSize(jdbc.getMaximumPoolSize());
            ds.setMinimumIdle(jdbc.getMinimumIdle());
            ds.setIdleTimeout(jdbc.getIdleTimeoutMs());
            ds.setMaxLifetime(jdbc.getMaxLifetimeMs());
            ds.setPoolName(jdbc.getPoolName());

            DATA_SOURCE = ds;

            LOG.info("HikariCP initialized (url={}, pool={}, maxPool={})",
                    ds.getJdbcUrl(), ds.getPoolName(), ds.getMaximumPoolSize());

        } catch (ClassNotFoundException | IllegalArgumentException | IllegalStateException e) {
            LOG.error("Failed to initialize HikariCP", e);
            throw new JdbcException("DB pool init failed", e);
        }
    }

    private JdbcConnectionFactory() {
    }

    public static Connection getConnection() throws SQLException {
        return DATA_SOURCE.getConnection();
    }
}