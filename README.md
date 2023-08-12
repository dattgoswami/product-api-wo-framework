# Simple Product API Server

This is a simple HTTP API server implemented using Python's built-in `http.server`. It provides basic CRUD operations for product data.

## Requirements

- Python 3.10

## Running the Server

To start the server, simply run:

```
python3 api_server.py
```

By default, the server will run on port 8080. If you wish to specify a different port, you can do so using the `PORT` environment variable:

```
PORT=8000 python api_server.py
```

## API Endpoints

- `GET /items`: Retrieve all products.
- `GET /items/<id>`: Retrieve a product by its ID.
- `POST /items`: Add a new product. Requires JSON payload with `name`, `price`, `url`, and `description`.
- `PUT /items/<id>`: Update an existing product by its ID.
- `DELETE /items/<id>`: Delete a product by its ID.

## Future Improvements

- Add a persistent database to store product data.
- Implement authentication and authorization.
- Extend the API to support more complex queries and operations.
