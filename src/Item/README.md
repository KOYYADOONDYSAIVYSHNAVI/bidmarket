# Deployment

```
docker compose up -d
```

The default exposed port is 8081. You can change it in the docker-compose.yml file.

# Usage

This is a REST API built on Flask that allows you to create, read, update, delete, and perform additional actions on
items. Below are the available endpoints:

## Endpoints

### **GET** `/items`

- **Description**: Fetch a list of all items.
- **Response**:
    - `200 OK`: Returns a list of all items.
    - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **GET** `/items/<item_id>`

- **Description**: Retrieve details of a specific item by its ID.
- **Path Parameters**:
    - `item_id` (required): The unique identifier of the item.
- **Response**:
    - `200 OK`: Returns the item details.
    - `404 Not Found`: Returns an error message if the item is not found.
    - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **GET** `/items/user/<user_id>`

- **Description**: Fetch all items associated with a specific user.
- **Path Parameters**:
    - `user_id` (required): The unique identifier of the user.
- **Response**:
    - `200 OK`: Returns a list of items belonging to the user.
    - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **GET** `/items/category/<category>`

- **Description**: Fetch all items belonging to a specific category.
- **Path Parameters**:
    - `category` (required): The category name.
- **Response**:
    - `200 OK`: Returns a list of items in the specified category.
    - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **GET** `/items/keyword/<keyword>`

- **Description**: Search for items by a keyword in their attributes.
- **Path Parameters**:
    - `keyword` (required): The keyword to search for.
- **Response**:
    - `200 OK`: Returns a list of matching items.
    - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **POST** `/items`
- **Description**: Create a new item.
- **Request Body** (JSON):
  ```json
  {
    "user_id": "1abc",
    "starting_price": 1.0,
    "quantity": 1,
    "shipping_cost": 1.0,
    "description": "New item",
    "flagged": false,
    "category": "New",
    "keywords": ["New", "Item"]
  }
  ```
- **Response**:
  - `201 Created`: Returns the ID of the newly created item.
  - `400 Bad Request`: Returns an error if the request body is invalid.
  - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **PUT** `/items/<item_id>`
- **Description**: Update the details of an existing item.
- **Path Parameters**:
  - `item_id` (required): The unique identifier of the item.
- **Request Body** (JSON):
  ```json
  {
    "user_id": "1abc",
    "starting_price": 1.0,
    "quantity": 1,
    "shipping_cost": 1.0,
    "description": "New item",
    "flagged": false,
    "category": "New",
    "keywords": ["New", "Item"]
  }
  ```
- **Response**:
  - `200 OK`: Returns the number of items updated.
  - `400 Bad Request`: Returns an error if the request body is invalid.
  - `404 Not Found`: Returns an error message if the item is not found.
  - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **PUT** `/items/flag/<item_id>`
- **Description**: Flag an item for review.
- **Path Parameters**:
  - `item_id` (required): The unique identifier of the item.
- **Response**:
  - `200 OK`: Returns the updated item details.
  - `404 Not Found`: Returns an error message if the item is not found.
  - `500 Internal Server Error`: Returns an error message if something goes wrong.

---

### **DELETE** `/items/<item_id>`
- **Description**: Delete an item by its ID.
- **Path Parameters**:
  - `item_id` (required): The unique identifier of the item.
- **Response**:
  - `200 OK`: Returns a confirmation message.
  - `404 Not Found`: Returns an error message if the item is not found.
  - `500 Internal Server Error`: Returns an error message if something goes wrong.
