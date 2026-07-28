package spring.dto;


import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;

public class OrderRequestDto {
    @NotBlank
    private String orderDate;
    @NotBlank
    private String deliveryAddress;
    @NotNull
    @Min(0)
    private Double sum;
    @NotNull
    private boolean state;
    @PositiveOrZero
    private Integer itemNumber;

    public @NotBlank String getOrderDate() {
        return orderDate;
    }

    public void setOrderDate(@NotBlank String orderDate) {
        this.orderDate = orderDate;
    }

    public @NotBlank String getDeliveryAddress() {
        return deliveryAddress;
    }

    public void setDeliveryAddress(@NotBlank String deliveryAddress) {
        this.deliveryAddress = deliveryAddress;
    }

    public @NotNull @Min(0) Double getSum() {
        return sum;
    }

    public void setSum(@NotNull @Min(0) Double sum) {
        this.sum = sum;
    }

    @NotNull
    public boolean isState() {
        return state;
    }

    public void setState(@NotNull boolean state) {
        this.state = state;
    }

    public @PositiveOrZero Integer getItemNumber() {
        return itemNumber;
    }

    public void setItemNumber(@PositiveOrZero Integer itemNumber) {
        this.itemNumber = itemNumber;
    }
}
