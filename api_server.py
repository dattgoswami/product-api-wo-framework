import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Initial data
data = [
    {
        "id": 1,
        "name": "Book",
        "price": 9.99,
        "url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "description": "You can read it!"
    },
    {
        "id": 2,
        "name": "Headphones",
        "price": 249.99,
        "url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "description": "Listen to stuff!"
    },
    {
        "id": 3,
        "name": "Backpack",
        "price": 79.99,
        "url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "description": "Carry things around town!"
    },
    {
        "id": 4,
        "name": "Glasses",
        "price": 129.99,
        "url": "https://images.unsplash.com/photo-1591076482161-42ce6da69f67?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "description": "Now you can see!"
    },
    {
        "id": 5,
        "name": "Cup",
        "price": 4.99,
        "url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "description": "Drink anything with it!"
    },
    {
        "id": 6,
        "name": "Shirt",
        "price": 29.99,
        "url": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=800&q=80",
        "description": "Wear it with style!"
    }
]


class ProductAPI(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        route_parts = parsed_path.path.strip("/").split("/")

        if len(route_parts) == 1 and route_parts[0] == "items":
            self._send_response(200, data)
        elif len(route_parts) == 2 and route_parts[0] == "items":
            try:
                item_id = int(route_parts[1])
                item = next(
                    (item for item in data if item["id"] == item_id), None)
                if item:
                    self._send_response(200, item)
                else:
                    self._send_response(404, {"error": "Not found"})
            except ValueError:
                self._send_response(400, {"error": "Bad request"})
        else:
            self._send_response(404, {"error": "Not found"})

    def do_POST(self):
        parsed_path = urlparse(self.path)
        route_parts = parsed_path.path.strip("/").split("/")

        if len(route_parts) == 1 and route_parts[0] == "items":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_item = json.loads(post_data)

            if not all(key in new_item for key in ["name", "price", "url", "description"]):
                self._send_response(400, {'error': 'Invalid item format'})
                return

            # Append to data and return
            data.append(new_item)
            self._send_response(201, new_item)
        else:
            self._send_response(404, {"error": "Not found"})


    def do_PUT(self):
        parsed_path = urlparse(self.path)
        route_parts = parsed_path.path.strip("/").split("/")

        if len(route_parts) == 2 and route_parts[0] == "items":
            try:
                item_id = int(route_parts[1])
                item = next((item for item in data if item["id"] == item_id), None)

                if not item:
                    self._send_response(404, {"error": "Not found"})
                    return

                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                update_data = json.loads(put_data)

                # Update the item
                item.update(update_data)
                self._send_response(200, item)

            except ValueError:
                self._send_response(400, {"error": "Bad request"})
        else:
            self._send_response(404, {"error": "Not found"})


    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        route_parts = parsed_path.path.strip("/").split("/")

        if len(route_parts) == 2 and route_parts[0] == "items":
            try:
                item_id = int(route_parts[1])
                global data
                new_data = [item for item in data if item["id"] != item_id]

                if len(new_data) == len(data):  # No item was deleted, as it wasn't found
                    self._send_response(404, {"error": "Not found"})
                    return

                data = new_data
                self._send_response(200, {"result": "Success"})

            except ValueError:
                self._send_response(400, {"error": "Bad request"})
        else:
            self._send_response(404, {"error": "Not found"})


    def _send_response(self, status, content):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProductAPI)
    print(f"Running on port {port}")
    httpd.serve_forever()
