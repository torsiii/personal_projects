package spring.web;

import spring.dto.OrderRequestDto;
import spring.dto.OrderResponseDto;
import spring.exception.ServiceException;
import spring.mapper.OrderMapper;
import spring.model.Order;
import spring.service.OrderService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    private final OrderService orderService;
    private final OrderMapper orderMapper;

    public OrderController(OrderService orderService, OrderMapper orderMapper) {
        this.orderService = orderService;
        this.orderMapper = orderMapper;
    }

    @GetMapping
    public ResponseEntity<List<OrderResponseDto>> getAll(
            @RequestParam(name = "orderDate", required = false) String orderDate
    ) throws ServiceException {
        List<Order> orders;

        if (orderDate == null || orderDate.isBlank()) {
            orders = orderService.listOrders();
        } else {
            orders = orderService.getOrdersByDate(orderDate);
        }

        List<OrderResponseDto> dtos = orders.stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());

        return ResponseEntity.ok(dtos);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderResponseDto> getById(@PathVariable Long id) throws ServiceException {
        Order order = orderService.getOrderById(id);

        if (order == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(orderMapper.toDto(order));
    }

    @PostMapping
    public ResponseEntity<OrderResponseDto> create(@Valid @RequestBody OrderRequestDto dto)
            throws ServiceException {
        Order model = orderMapper.toModel(dto);

        orderService.placeOrder(model);

        return ResponseEntity.status(201).body(orderMapper.toDto(model));
    }

    @PutMapping("/{id}")
    public ResponseEntity<OrderResponseDto> update(
            @PathVariable Long id,
            @Valid @RequestBody OrderRequestDto dto
    ) throws ServiceException {
        Order existing = orderService.getOrderById(id);

        if (existing == null) {
            return ResponseEntity.notFound().build();
        }

        orderMapper.updateModel(existing, dto);
        orderService.updateOrder(id, existing);

        return ResponseEntity.ok(orderMapper.toDto(existing));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) throws ServiceException {
        Order existing = orderService.getOrderById(id);

        if (existing == null) {
            return ResponseEntity.notFound().build();
        }

        orderService.deleteOrder(id);

        return ResponseEntity.noContent().build();
    }
}