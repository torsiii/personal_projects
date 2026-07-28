package spring.dto;

public class OrderResponseDto {
    private Long id;
    private String orderDate;
    private String deliveryAddress;
    private Double sum;
    private boolean state;
    private Integer itemNumber;

    public OrderResponseDto() {
    }

    public OrderResponseDto(Long id, String orderDate, String deliveryAddress,
                            Double sum, boolean state, Integer itemNumber) {
        this.id = id;
        this.orderDate = orderDate;
        this.deliveryAddress = deliveryAddress;
        this.sum = sum;
        this.state = state;
        this.itemNumber = itemNumber;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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
}
