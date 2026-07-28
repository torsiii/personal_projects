package web;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import backend.exception.ServiceException;
import backend.model.Order;
import backend.repo.DaoFactory;
import backend.service.WebShop;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@WebServlet("/orders")
public class OrderServlet extends HttpServlet {
    private static final Logger LOG = LoggerFactory.getLogger(OrderServlet.class);

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper()
            .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

    private transient WebShop orderService;

    @Override
    public void init() {
        var dao = DaoFactory.getInstance().getOrderDao();
        orderService = new WebShop(dao);
    }

    private void setupJsonResponse(HttpServletResponse resp) {
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
    }

    private Long parseIdOrSendError(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String idParam = req.getParameter("id");
        if (idParam == null || idParam.isBlank()) {
            writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, "Missing id parameter");
            return null;
        }

        try {
            return Long.valueOf(idParam.trim());
        } catch (NumberFormatException e) {
            writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, "Invalid id parameter: " + idParam);
            return null;
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        setupJsonResponse(resp);

        String idParam = req.getParameter("id");

        try {
            if (idParam == null) {
                List<Order> orders = orderService.listOrders();
                OBJECT_MAPPER.writeValue(resp.getWriter(), orders);
            } else {
                Long id = parseIdOrSendError(req, resp);
                if (id == null) {
                    return;
                }

                Order order = orderService.getOrderById(id);
                if (order == null) {
                    LOG.warn("Order not found (id={})", id);
                    writeJsonError(resp, HttpServletResponse.SC_NOT_FOUND, "Order not found");
                } else {
                    OBJECT_MAPPER.writeValue(resp.getWriter(), order);
                }
            }
        } catch (ServiceException e) {
            LOG.error("Service error during GET /orders", e);
            writeJsonError(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Service error");
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        setupJsonResponse(resp);

        try {
            Order order = OBJECT_MAPPER.readValue(req.getReader(), Order.class);

            String validationError = validateOrder(order);
            if (validationError != null) {
                writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, validationError);
                return;
            }

            orderService.placeOrder(order);

            resp.setStatus(HttpServletResponse.SC_CREATED);
            OBJECT_MAPPER.writeValue(resp.getWriter(), order);

        } catch (JsonProcessingException e) {
            LOG.warn("POST /orders invalid JSON body", e);
            writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, "Invalid JSON body");
        } catch (ServiceException e) {
            LOG.error("ServiceException during POST /orders", e);
            writeJsonError(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Service error");
        }
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        setupJsonResponse(resp);

        Long id = parseIdOrSendError(req, resp);
        if (id == null) {
            return;
        }

        try {
            Order existing = orderService.getOrderById(id);
            if (existing == null) {
                LOG.warn("PUT /orders - order not found (id={})", id);
                writeJsonError(resp, HttpServletResponse.SC_NOT_FOUND, "Order not found");
                return;
            }

            Order updated = OBJECT_MAPPER.readValue(req.getReader(), Order.class);

            String validationError = validateOrder(updated);
            if (validationError != null) {
                writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, validationError);
                return;
            }

            updated.setId(id);
            orderService.updateOrder(id, updated);

            resp.setStatus(HttpServletResponse.SC_OK);
            OBJECT_MAPPER.writeValue(resp.getWriter(), updated);

        } catch (JsonProcessingException e) {
            LOG.warn("PUT /orders invalid JSON body (id={})", id, e);
            writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, "Invalid JSON body");
        } catch (ServiceException e) {
            LOG.error("ServiceException during PUT /orders (id={})", id, e);
            writeJsonError(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Service error");
        }
    }

    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        setupJsonResponse(resp);

        Long id = parseIdOrSendError(req, resp);
        if (id == null) {
            return;
        }

        try {
            Order existing = orderService.getOrderById(id);
            if (existing == null) {
                LOG.warn("DELETE /orders - order not found (id={})", id);
                writeJsonError(resp, HttpServletResponse.SC_NOT_FOUND, "Order not found");
                return;
            }

            orderService.deleteOrder(id);
            resp.setStatus(HttpServletResponse.SC_NO_CONTENT);

        } catch (ServiceException e) {
            LOG.error("ServiceException during DELETE /orders (id={})", id, e);
            writeJsonError(resp, HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Service error");
        }
    }

    private String validateOrder(Order order) {
        if (order == null) {
            return "Request body is required";
        }
        if (order.getOrderDate() == null || order.getOrderDate().isBlank()) {
            return "Missing required field: orderDate";
        }
        if (order.getDeliveryAddress() == null || order.getDeliveryAddress().isBlank()) {
            return "Missing required field: deliveryAddress";
        }
        if (order.getSum() == null) {
            return "Missing required field: sum";
        }
        if (order.getItemNumber() == null) {
            return "Missing required field: itemNumber";
        }
        return null;
    }

    private void writeJsonError(HttpServletResponse resp, int status, String message) throws IOException {
        setupJsonResponse(resp);
        resp.setStatus(status);
        OBJECT_MAPPER.writeValue(resp.getWriter(), Map.of("error", message));
    }
}