# Bidmarket

# High-Level Architecture Model

## 1. Presentation Layer (Frontend)
- **HTML + React**  
  - Handles user interaction and presentation logic.  
  - Communicates with backend services via REST APIs.

## 2. Application Layer (Backend Services)
- **Auction Service**  
  - Manages auction creation, bidding, and closing.  
  - Interacts with Item and User services for validating operations.

- **Item Service**  
  - Handles item listings, metadata, and search functionality.  
  - Interfaces with MongoDB for storing item data.

- **User Service**  
  - Manages user profiles, authentication, and authorization.  
  - Interfaces with MySQL for relational data storage.

- **Admin Service**  
  - Provides administrative tools for managing users, auctions, and notifications.  
  - Triggers email notifications through the Google SMTP server.

- **Notification Service**  
  - Sends real-time notifications using RabbitMQ.

## 3. Data Layer
- **MySQL Database**  
  - Stores user data.

- **MongoDB**  
  - Stores non-relational data, such as items, auctions, and emails.

## 4. Communication
- **REST API**  
  - Used for communication between the frontend and backend services.

- **gRPC**  
  - Used for internal communication between microservices to ensure high performance and low latency.

## 5. Integration Layer
- **RabbitMQ**  
  - Handles asynchronous message delivery for the Notification Service.  
  - Ensures that users receive updates on bids, auctions, and administrative alerts.

- **SMTP Google Server**  
  - Sends support email notifications.

---

## Flow of Data and Communication

### User Interaction:
- A user accesses the site via a browser (React frontend).
- The frontend sends a REST API request to the backend services.

### Backend Processing:
- Backend services communicate internally using gRPC to fetch or update data across User, Item, and Auction services.

### Data Persistence:
- MySQL stores relational data (e.g., user profiles).
- MongoDB stores non-relational data (e.g., item, auction).

### Notification:
- The Notification Service publishes messages to RabbitMQ for real-time updates.
- If an email is required, it uses the Google SMTP server.
