package spring.exception;

public class ServiceException extends Exception {
    private final String info;

    public ServiceException(String info) {
        super(info);
        this.info = info;
    }

    public String getInfo() {
        return info;
    }
}