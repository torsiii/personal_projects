package web;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.util.Map;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {
    private static final String USERNAME = "your_username";
    private static final String PASSWORD = "your_password";
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        setupJsonResponse(resp);

        try {
            LoginRequest loginRequest = OBJECT_MAPPER.readValue(req.getReader(), LoginRequest.class);

            if (loginRequest.getUsername() == null || loginRequest.getPassword() == null) {
                writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST,
                        "username and password are required");
                return;
            }

            if (USERNAME.equals(loginRequest.getUsername())
                    && PASSWORD.equals(loginRequest.getPassword())) {
                HttpSession session = req.getSession(true);
                session.setAttribute("loggedInUser", loginRequest.getUsername());

                resp.setStatus(HttpServletResponse.SC_OK);
                OBJECT_MAPPER.writeValue(resp.getWriter(),
                        Map.of("message", "Login successful"));
            } else {
                writeJsonError(resp, HttpServletResponse.SC_UNAUTHORIZED,
                        "Invalid username or password");
            }

        } catch (JsonProcessingException e) {
            writeJsonError(resp, HttpServletResponse.SC_BAD_REQUEST, "Invalid JSON body");
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        setupJsonResponse(resp);

        HttpSession session = req.getSession(false);
        boolean loggedIn = session != null && session.getAttribute("loggedInUser") != null;

        resp.setStatus(HttpServletResponse.SC_OK);
        OBJECT_MAPPER.writeValue(resp.getWriter(), Map.of("loggedIn", loggedIn));
    }

    private void setupJsonResponse(HttpServletResponse resp) {
        resp.setContentType("application/json");
        resp.setCharacterEncoding("UTF-8");
    }

    private void writeJsonError(HttpServletResponse resp, int status, String message) throws IOException {
        setupJsonResponse(resp);
        resp.setStatus(status);
        OBJECT_MAPPER.writeValue(resp.getWriter(), Map.of("error", message));
    }
}