package backend.repo.mem;

import backend.exception.DataAccessException;
import backend.model.BaseEntity;
import backend.repo.Dao;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public abstract class MemDao<T extends BaseEntity> implements Dao<T> {

    protected Map<Long, T> entities = new ConcurrentHashMap<>();
    private Long idCounter = 0L;

    @Override
    public void create(T entity) {
        ++idCounter;
        entity.setId(idCounter);
        entities.put(entity.getId(), entity);
    }


    @Override
    public void update(String id, T entity) throws DataAccessException {
        final long longId = Long.parseLong(id.trim());

        entity.setId(longId);
        if (!entities.containsKey(longId)) {
            throw new DataAccessException("Entity not found with id=" + id);
        }
        entities.put(longId, entity);
    }

    @Override
    public void delete(String id) throws DataAccessException {
        final long longId = Long.parseLong(id.trim());

        if (entities.remove(longId) == null) {
            throw new DataAccessException("Entity not found with id=" + id);
        }
    }

    @Override
    public List<T> read() throws DataAccessException {

        return List.copyOf(entities.values());
    }

    @Override
    public T findById(String id) throws DataAccessException {
        try {
            long longId = Long.parseLong(id.trim());
            return entities.get(longId);
        } catch (NumberFormatException e) {
            throw new DataAccessException("Invalid id: " + id);
        }
    }

}
