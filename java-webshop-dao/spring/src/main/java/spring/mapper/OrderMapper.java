package spring.mapper;

import spring.dto.OrderRequestDto;
import spring.dto.OrderResponseDto;
import spring.model.Order;

@org.springframework.stereotype.Component
public class OrderMapper {
    public Order toModel(OrderRequestDto dto) {
        if (dto == null) {
            return null;
        }

        return new Order(
                dto.getOrderDate(),
                dto.getDeliveryAddress(),
                dto.getSum(),
                dto.isState(),
                dto.getItemNumber()
        );
    }

    public void updateModel(Order model, OrderRequestDto dto) {
        model.setOrderDate(dto.getOrderDate());
        model.setDeliveryAddress(dto.getDeliveryAddress());
        model.setSum(dto.getSum());
        model.setState(dto.isState());
        model.setItemNumber(dto.getItemNumber());
    }

    public OrderResponseDto toDto(Order model) {
        if (model == null) {
            return null;
        }

        return new OrderResponseDto(
                model.getId(),
                model.getOrderDate(),
                model.getDeliveryAddress(),
                model.getSum(),
                model.isState(),
                model.getItemNumber()
        );
    }
}