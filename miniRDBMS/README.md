# Mini Relational Database Management System

A university project developed to explore how the core concepts of a **relational database management system (RDBMS)** can be implemented on top of a document-oriented storage engine.

The application provides a custom database layer with relational-style schemas, constraints, indexes, queries, joins, grouping, and aggregation. MongoDB is used as the underlying persistence mechanism, while the relational behavior is implemented in Python by the application itself.

## Project Purpose

The main goal of the project was to understand and implement fundamental database-management concepts rather than relying entirely on built-in relational database functionality.

The system demonstrates how an application can manage:

- databases and tables;
- table metadata and column definitions;
- primary-key uniqueness;
- unique and foreign-key constraints;
- cascading deletion;
- custom indexes;
- filtered queries and projections;
- multi-table joins;
- grouping, aggregate functions, `HAVING`, and ordering;
- communication between a graphical client and a database server.

## Key Features

### Database and schema management

- Create and drop databases
- Create and drop tables
- Define typed columns using `int`, `float`, and `string`
- Store schema definitions in both JSON metadata and MongoDB metadata collections
- List available databases and tables

### Data manipulation

- Insert records
- Delete records by primary key
- Validate duplicate primary keys
- Enforce unique constraints
- Validate foreign-key references
- Cascade deletes to dependent records

### Query functionality

- Select all or specific columns
- Apply multiple `WHERE` conditions
- Supported comparison operators:
  - `=`
  - `>`
  - `>=`
  - `<`
  - `<=`
- Detect impossible numeric range conditions
- Remove duplicate projected results
- Perform multi-table join queries
- Apply conditions independently to joined tables

### Aggregation and sorting

- `GROUP BY`
- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`
- `HAVING`
- Ascending and descending `ORDER BY`

### Custom indexing

The project implements application-managed indexes using separate MongoDB collections. Both unique and non-unique indexes are supported.

When an indexed column appears in a query condition, the server uses the relevant index collection to reduce the candidate record set. When no suitable index exists, the system falls back to scanning the table.

### Client-server architecture

The application follows a simple client-server model:

```text
Tkinter GUI Client
        │
        │ JSON commands over TCP sockets
        ▼
Python Database Server
        │
        ├── Relational logic and constraint validation
        ├── Schema metadata management
        ├── Query and index processing
        ▼
MongoDB Storage Engine
```

The graphical client sends JSON commands to the server through a TCP socket. The server interprets each command, performs the requested database operation, and returns the result to the client.

## Technologies Used

- **Python 3** – application logic
- **MongoDB** – underlying persistent storage
- **PyMongo** – MongoDB connectivity
- **Tkinter** – desktop graphical user interface
- **Python sockets** – TCP client-server communication
- **JSON** – command exchange and schema metadata storage
- **Faker** – generation of sample data
- **Colorama / Termcolor** – formatted terminal output

## Requirements

Before running the project, install:

- Python 3.10 or newer
- MongoDB Community Server
- The required Python packages

```bash
pip install pymongo faker colorama termcolor
```

Ensure that MongoDB is running locally on its default address:

```text
mongodb://localhost:27017/
```

## Running the Application

### 1. Start MongoDB

Start your local MongoDB service before launching the application.

### 2. Start the database server

```bash
python server_cli.py
```

The server listens on TCP port `12345`.

### 3. Start the graphical client

Open another terminal and run:

```bash
python clientgui_final.py
```

The client connects to:

```text
localhost:12345
```

You can then create databases and tables, insert or delete records, build indexes, execute selections, and create join queries through the graphical interface.

## High-Volume Testing

The project includes a configurable data-generation utility for testing the system with large datasets:

```bash
python test.py <database_name> <table_name> <row_count>
```

Example:

```bash
python test.py benchmark records 100000
```

The generator reads the selected table's metadata and creates values that match its declared column types. The desired number of records is provided as a command-line argument, which makes it possible to test the system with datasets of different sizes.

During development, the application was tested with high row counts to verify that inserts and queries continued to produce correct results on larger datasets and completed within a practical amount of time. Progress reporting is included for long data-generation runs.

This testing was especially useful for comparing:

- indexed queries with full table scans;
- equality and range filtering;
- query behavior on large result sets;
- join and aggregation operations;
- correctness of metadata and constraint handling under increased data volume.

## Example Workflow

1. Create a database.
2. Create one or more tables with typed columns.
3. Define unique or foreign-key constraints where required.
4. Insert records through the GUI.
5. Create an index for frequently queried columns.
6. Run a filtered `SELECT` query.
7. Join related tables.
8. Apply grouping, aggregate functions, `HAVING`, or ordering.
9. Generate a larger dataset with `test.py` and repeat the queries.

## Design Notes

MongoDB stores each logical row as a document containing:

- `_id` – the primary key;
- `value` – the row values serialized into a delimiter-separated string.

Table definitions are stored separately as metadata. The server uses this metadata to reconstruct typed rows, validate constraints, process joins, and determine whether a query can use an application-managed index.

This architecture was intentionally chosen as a learning exercise: relational behavior is implemented explicitly in the Python server instead of being delegated to a traditional SQL database engine.

## Limitations

As an educational mini-RDBMS, the project has several limitations:

- It supports a deliberately limited subset of SQL-like operations.
- Queries are constructed through JSON commands and the GUI rather than an SQL parser.
- Transactions, concurrency control, authentication, and access permissions are not implemented.
- Row serialization uses a custom delimiter-based representation.
- The server handles connections sequentially and is intended for local demonstration.
- Benchmark results are environment-dependent and are not a substitute for formal performance testing.
