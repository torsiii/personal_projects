# Java WebShop DAO Application

A Java-based order management application demonstrating **layered architecture**, the **DAO (Data Access Object) design pattern**, configurable persistence mechanisms, JDBC database access, servlet-based REST APIs, session authentication, and a Swing desktop user interface.

The application supports both **in-memory** and **PostgreSQL-backed** persistence, allowing the active implementation to be selected at runtime through configuration.

---

## Features

- CRUD operations for orders
- Generic DAO abstraction
- Runtime-selectable persistence layer
- In-memory storage implementation
- PostgreSQL database support
- JDBC-based data access
- HikariCP connection pooling
- Servlet-based REST API
- Session-based authentication
- Authentication filter for protected resources
- Swing desktop application
- JSON-based configuration
- Layered application architecture
- Custom exception hierarchy
- SLF4J logging

---

## Technologies

- Java
- Jakarta Servlet API
- JDBC
- PostgreSQL
- HikariCP
- Jackson
- SLF4J
- Swing
- Gradle
- Apache Tomcat

---

## Architecture

The project follows a classic layered architecture:

```text
Presentation Layer
        │
Service Layer
        │
DAO Abstraction
        │
Persistence Layer
```

### Model Layer

Contains the application's domain entities.

**Main classes**

- `BaseEntity`
- `Order`

---

### Repository Layer

Defines a generic DAO interface and repository-specific operations.

**Core components**

- `Dao<T>`
- `OrderDao`
- `DaoFactory`

Two interchangeable persistence implementations are provided:

- Memory DAO
- JDBC DAO

The active implementation is selected automatically based on the configured application profile.

---

### Service Layer

Contains the application's business logic.

**Main classes**

- `OrderService`
- `WebShop`

The service layer is independent of the persistence technology and translates repository exceptions into service-level exceptions.

---

### Presentation Layer

The application provides two independent user interfaces:

- Swing desktop application
- Servlet-based REST API

---

## Order Model

Each order contains the following fields:

| Field | Type | Description |
|--------|------|-------------|
| id | Long | Unique identifier |
| orderDate | String | Order date |
| deliveryAddress | String | Delivery address |
| sum | Double | Total order value |
| state | boolean | Order status |
| itemNumber | Integer | Number of ordered items |

### Example JSON

```json
{
  "orderDate": "2026-07-28",
  "deliveryAddress": "Example Street 10",
  "sum": 149.99,
  "state": false,
  "itemNumber": 3
}
```

---

## Configuration

The application supports two runtime profiles:

- `memory`
- `jdbc`

The active profile is selected in the following order:

1. Java system property (`app.profile`)
2. Environment variable (`APP_PROFILE`)
3. Default profile (`memory`)

---

### Memory Profile

Stores data in a thread-safe in-memory collection.

Configuration file:

```text
app-memory.json
```

Example:

```json
{
  "daoType": "MEMORY"
}
```

---

### JDBC Profile

Stores orders in a PostgreSQL database.

Configuration file:

```text
app-jdbc.json
```

Example:

```json
{
  "daoType": "JDBC",
  "jdbc": {
    "url": "jdbc:postgresql://localhost:5432/webshop",
    "username": "your_username",
    "password": "your_password",
    "maximumPoolSize": 10,
    "minimumIdle": 2,
    "idleTimeoutMs": 60000,
    "maxLifetimeMs": 1800000,
    "poolName": "WebShopPool",
    "driverClassName": "org.postgresql.Driver"
  }
}
```

## Database Setup

Create the database:

```sql
CREATE DATABASE webshop;
```

Create the `orders` table:

```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_date VARCHAR(50) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
    sum DOUBLE PRECISION NOT NULL,
    state BOOLEAN NOT NULL,
    item_number INTEGER NOT NULL
);
```

Update the local JDBC configuration with your database credentials.

---

## Running the Application

### Swing Desktop Application

Main class:

```text
desktop.Main
```

### Memory Profile

```bash
./gradlew run
```

or

```bash
java -Dapp.profile=memory -jar application.jar
```

---

### JDBC Profile

#### Linux / macOS

```bash
APP_PROFILE=jdbc ./gradlew run
```

#### Windows Command Prompt

```cmd
set APP_PROFILE=jdbc
gradlew run
```

#### Windows PowerShell

```powershell
$env:APP_PROFILE = "jdbc"
./gradlew run
```

or

```bash
java -Dapp.profile=jdbc -jar application.jar
```

---

## REST API

Deploy the generated WAR file to a Jakarta-compatible servlet container (e.g. Apache Tomcat).

---

### Authentication

#### Login

```http
POST /login
```

Request:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "message": "Login successful"
}
```

Authentication state is stored in the HTTP session.

Protected endpoints require an authenticated session.

Unauthorized requests receive:

```json
{
  "error": "Authentication required"
}
```

> **Note**
>
> Authentication is implemented for educational purposes.

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/login` | Check login status |
| POST | `/login` | Authenticate user |
| GET | `/orders` | List all orders |
| GET | `/orders?id=1` | Retrieve order by ID |
| POST | `/orders` | Create order |
| PUT | `/orders?id=1` | Update order |
| DELETE | `/orders?id=1` | Delete order |

---

### Create Order

```http
POST /orders
Content-Type: application/json
```

```json
{
  "orderDate": "2026-07-28",
  "deliveryAddress": "Example Street 10",
  "sum": 149.99,
  "state": false,
  "itemNumber": 3
}
```

Response:

```http
201 Created
```

---

### Update Order

```http
PUT /orders?id=1
```

```json
{
  "orderDate": "2026-07-29",
  "deliveryAddress": "Updated Street 20",
  "sum": 189.99,
  "state": true,
  "itemNumber": 4
}
```

---

### Delete Order

```http
DELETE /orders?id=1
```

Response:

```http
204 No Content
```

---

## DAO Pattern

The application is built around a generic DAO abstraction.

```java
public interface Dao<T extends BaseEntity> {
    void create(T entity);
    void update(String id, T entity);
    void delete(String id);
    List<T> read();
}
```

`OrderDao` extends the generic interface with repository-specific operations.

```java
Collection<Order> findByOrderDate(String date);

Order findByDeliveryAddress(String address);
```

The selected implementation is created through `DaoFactory`.

```text
DaoFactory
├── MemDaoFactory
└── JdbcDaoFactory
```

This approach keeps the service layer independent of the underlying persistence technology.

---

## Connection Pooling

The JDBC implementation uses **HikariCP**.

Supported configuration includes:

- Maximum pool size
- Minimum idle connections
- Idle timeout
- Maximum connection lifetime
- Pool name
- JDBC driver

Database resources are managed using Java's **try-with-resources** mechanism.

---

## Error Handling

The project defines custom exception types to separate concerns between layers.

- ConfigLoadException
- JdbcException
- DataAccessException
- ServiceException

Repository exceptions are converted into `DataAccessException`.

Service-layer exceptions are converted into `ServiceException`.

REST endpoints return structured JSON error responses together with appropriate HTTP status codes.

Example:

```json
{
  "error": "Missing required field: deliveryAddress"
}
```

---

## Logging

Logging is implemented using **SLF4J**.

Logged events include:

- Configuration loading
- DAO initialization
- Connection pool creation
- CRUD operations
- Database queries
- Service errors
- Servlet errors

Sensitive information such as passwords, session identifiers, and authentication tokens is never logged.

---

## Security Considerations

Before publishing or deploying the application:

- Remove real database credentials
- Avoid hardcoded passwords
- Exclude local configuration files
- Ignore `.env` files
- Never log sensitive information
- Hash passwords securely
- Use HTTPS
- Configure secure session cookies
- Validate all incoming request data

---

## Build

Run a full build before committing:

```bash
./gradlew clean build
```

Windows:

```cmd
gradlew clean build
```

---

## Educational Purpose

This project demonstrates:

- Object-oriented programming
- Layered software architecture
- DAO design pattern
- Factory pattern
- JDBC database access
- Connection pooling
- Servlet development
- Session-based authentication
- JSON serialization
- Swing desktop application development

---
