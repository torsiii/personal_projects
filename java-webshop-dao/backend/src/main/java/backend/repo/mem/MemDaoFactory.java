package backend.repo.mem;

import backend.repo.DaoFactory;
import backend.repo.OrderDao;

public class MemDaoFactory extends DaoFactory {

    private static final OrderDao ORDER_DAO = new OrderMemDao();

    @Override
    public OrderDao getOrderDao() {
        return ORDER_DAO;
    }
}