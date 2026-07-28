package backend.model;

public class Order extends BaseEntity {
    private String orderDate;
    private String deliveryAddress;
    private Double sum;
    private boolean state;
    private Integer itemNumber;

    public Order() {
        super();
    }

    public Order(Long id, String orderDate, String deliveryAddress, Double sum, boolean state, Integer itemNumber) {
        super(id);
        this.orderDate = orderDate;
        this.deliveryAddress = deliveryAddress;
        this.sum = sum;
        this.state = state;
        this.itemNumber = itemNumber;
    }

    public Order(String orderDate, String deliveryAddress, Double sum, boolean state, Integer itemNumber) {
        super();
        this.orderDate = orderDate;
        this.deliveryAddress = deliveryAddress;
        this.sum = sum;
        this.state = state;
        this.itemNumber = itemNumber;
    }

    public String getOrderDate() {
        return orderDate;
    }

    public void setOrderDate(String orderDate) {
        this.orderDate = orderDate;
    }

    public String getDeliveryAddress() {
        return deliveryAddress;
    }

    public void setDeliveryAddress(String deliveryAddress) {
        this.deliveryAddress = deliveryAddress;
    }

    public Double getSum() {
        return sum;
    }

    public void setSum(Double sum) {
        this.sum = sum;
    }

    public boolean isState() {
        return state;
    }

    public void setState(boolean state) {
        this.state = state;
    }

    public Integer getItemNumber() {
        return itemNumber;
    }

    public void setItemNumber(Integer itemNumber) {
        this.itemNumber = itemNumber;
    }

    @Override
    public String toString() {
        return "Order{"
                +
                "orderDate='" + orderDate + '\''
                +
                ", deliveryAddress='" + deliveryAddress + '\''
                +
                ", sum=" + sum
                +
                ", state=" + state
                +
                ", itemNumber=" + itemNumber
                +
                '}';
    }
}
