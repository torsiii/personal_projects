CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_date VARCHAR(100) NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
    sum DOUBLE PRECISION NOT NULL,
    state BOOLEAN NOT NULL,
    item_number INTEGER NOT NULL
);