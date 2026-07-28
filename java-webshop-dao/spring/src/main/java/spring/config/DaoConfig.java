
package spring.config;

import spring.repo.OrderDao;
import spring.repo.OrderJdbcDao;
import spring.repo.OrderMemDao;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

import javax.sql.DataSource;

@Configuration
public class DaoConfig {

    @Bean
    @Profile("mem")
    public OrderDao inMemoryOrderDao() {
        return new OrderMemDao();
    }

    @Bean
    @Profile("jdbc")
    public OrderDao jdbcOrderDao(DataSource dataSource) {
        return new OrderJdbcDao(dataSource);
    }
}