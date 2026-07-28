package spring.repo;


import spring.exception.DataAccessException;
import spring.model.BaseEntity;

import java.util.List;

public interface Dao<T extends BaseEntity> {

    void create(T entity) throws DataAccessException;

    void update(String id, T entity) throws DataAccessException;

    void delete(String id) throws DataAccessException;

    List<T> read() throws DataAccessException;

    T findById(String id) throws DataAccessException;

}
