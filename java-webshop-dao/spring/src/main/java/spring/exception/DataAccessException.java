package spring.exception;

public class DataAccessException extends Exception {

    private final String info;

    public DataAccessException(String info) {
        super(info);
        this.info = info;
    }

    public String getInfo() {
        return info;
    }
}