# Microservices, API Gateway, Authentication with FastAPI, non-blocking i/o

- This repo is composed of a bunch of small microservices considering API gateway approach
- Expected number of microservices was two, but considering that services
  should not create dependency on each other to prevent SPOF, also to prevent duplicate codes,
  I decided to put one API gateway in front that does JWT authentication for both services
  which I am inspired by Netflix/Zuul
- We have 3 services including gateway.
- Only gateway can access internal microservices through the internal network (users, orders)

## Project Structure

```
microservices_app/
│
├── README.md                 # Project documentation
├── docker-compose.yml        # Docker Compose configuration for all services
├──helm/                  # API Gateway Service
│   ├── gateway/                  # Gateway Service Helm chart
│   │   ├── Chart.yaml          # Helm chart metadata
│   │   ├── values.yaml         # Default configuration values for the chart
│   │   ├── templates/          # Kubernetes manifests for the gateway service
│   │   │   ├── deployment.yaml  # Deployment configuration for the gateway service
│   │   │   ├── service.yaml     # Service configuration for the gateway service
│   │   │   └── _helpers.tpl    # Ingress configuration for the gateway
│   └── users/                   # Users Service Helm chart
│       ├── Chart.yaml          # Helm chart metadata
│       ├── values.yaml         # Default configuration values for the chart
│       ├── templates/          # Kubernetes manifests for the users service
│       │   ├── deployment.yaml  # Deployment configuration for the users service
│       │   ├── service.yaml     # Service configuration for the users service
│       │   └── _helpers.tpl    # Ingress configuration for the users service
│       └── orders/              # Orders Service Helm chart
│           ├── Chart.yaml      # Helm chart metadata
│           ├── values.yaml     # Default configuration values for the chart
│           ├── templates/      # Kubernetes manifests for the orders service
│           │   ├── deployment.yaml  # Deployment configuration for the orders service
│           │   ├── service.yaml     # Service configuration for the orders service
│           │   └── _helpers.tpl    # Ingress configuration for the orders service
│    └── microservices-app/           # Microservices Helm chart
│        ├── Chart.yaml          # Helm chart metadata for the entire microservices app
│        ├── values.yaml         # Default configuration values for the entire app
│        ├── templates/          # Kubernetes manifests for the entire app
│        │   ├── deployement.yaml     
│        │   ├── service.yaml     
│        │   └── _helpers.tpl    # Ingress configuration for the entire app              
── Jenkins/ 
│   ├── build/
         ├── gateway/                  
               ├── Jenkinsfile
         ├── users/ 
                ├── Jenkinsfile
         ├── orders/  
                ├── Jenkinsfile
    ├── deploy/
         ├── gateway/                 
               ├── Jenkinsfile
         ├── users/ 
                ├── Jenkinsfile
         ├── orders/  
                ├── Jenkinsfile
    ├── jenkins-master/
         ├── gateway/                  
               ├── Jenkinsfile
         ├── users/ 
                ├── Jenkinsfile
         ├── orders/  
                ├── Jenkinsfile 
│── k8s/ 
│   ├── namespace.yaml 
    |──  networkpolicy.yaml    
├
├── gateway/                  # API Gateway Service
│   ├── Dockerfile            # Docker configuration for gateway service
│   ├── __init__.py
│   ├── auth.py               # Authentication and authorization functions
│   ├── conf.py               # Configuration settings
│   ├── core.py               # Core functionality including route decorator
│   ├── exceptions.py         # Custom exception handlers
│   ├── main.py               # Main FastAPI application with route definitions
│   ├── network.py            # Network communication utilities
│   ├── post_processing.py    # Post-processing functions for API responses
│   ├── requirements.txt      # Python dependencies for gateway service
│   └── datastructures/       # Data models for request/response validation
│       ├── orders.py         # Order-related data models
│       └── users.py          # User-related data models
│
├── orders/                   # Orders Microservice
│   ├── Dockerfile            # Docker configuration for orders service
│   ├── __init__.py
│   ├── init_db.py            # Database initialization script
│   ├── main.py               # Main FastAPI application with order endpoints
│   ├── models.py             # Database models using Tortoise ORM
│   └── requirements.txt      # Python dependencies for orders service
│
└── users/                    # Users Microservice
    ├── Dockerfile            # Docker configuration for users service
    ├── __init__.py
    ├── auth.py               # User authentication utilities
    ├── datastructures.py     # User-related data models
    ├── main.py               # Main FastAPI application with user endpoints
    ├── requirements.txt      # Python dependencies for users service
    ├── fake/                 # Fake database implementation
    │   ├── __init__.py
    │   ├── db.py             # Database operations for users
    │   └── users.json        # JSON file storing user data
    └── tests/                # Test modules
        ├── __init__.py
        ├── auth.py           # Authentication tests
        └── fake_db.py        # Fake database tests
```

## Services

### Gateway Service
- Built on top of FastAPI, simple API gateway which its only duty is to make proper routing while also handling authentication and authorization
- Acts as a central entry point for all client requests
- Handles JWT token generation and validation
- Routes requests to the appropriate microservice
- Implements a custom `route` decorator for declarative routing
- Provides endpoints for user management, authentication, and order management
- Uses non-blocking I/O with aiohttp for communication with microservices

### Users Service (a.k.a. admin)
- Keeps user info in its own fake db (file system)
- Can be executed simple CRUD operations through the service
- There is also another endpoint for login, but client is abstracted from real response. Thus, gateway service will handle login response and generate JWT token accordingly
- Provides endpoints for:
  - User authentication (login)
  - User creation, retrieval, update, and deletion
- Uses a file-based JSON database for storing user information
- Has protection for certain user IDs that cannot be deleted

### Orders Service
- Users (subscribed ones – authentication) can create and view (their – authorization) orders
- Provides endpoints for:
  - Creating new orders
  - Retrieving orders for the authenticated user
- Uses Tortoise ORM with SQLite in-memory database
- Identifies users through the request_user_id header passed from the gateway

## Running
- check ./gateway/.env → 2 services URL are defined based on twelve-factor config
- docker-compose up --build
- visit → http://localhost:8001/docs

## Example requests
- There are already created 2 users in users db
- get API token with admin user
  ```
  curl --header "Content-Type: application/json" \
       --request POST \
       --data '{"username":"admin","password":"a"}' \
       http://localhost:8001/api/login
  ```
- You'll see something similar to below
  ```
  {"access_token":"***","token_type":"bearer"}
  ```
- use this token to make administrative level requests
  ```
  curl --header "Content-Type: application/json" \
       --header "Authorization: Bearer ***" \
       --request GET \
       http://localhost:8001/api/users
  ```
- Similar trials can be also done with default user to create & view orders

## Technical Implementation Details

### API Gateway Pattern
- The gateway service implements the API Gateway pattern, acting as a single entry point for all client requests
- It handles cross-cutting concerns like authentication and authorization
- Routes requests to the appropriate microservice based on the path
- Provides a unified API for clients

### Authentication and Authorization
- JWT tokens are used for authentication
- The gateway service generates and validates JWT tokens
- Authorization is handled at the gateway level
- Microservices receive a request-user-id header to identify the user

### Non-blocking I/O
- Coroutines are used for I/O operations to boost performance
- aiohttp is used for non-blocking HTTP requests
- Tortoise ORM provides non-blocking database access

### Data Flow
1. Client sends a request to the gateway service
2. Gateway authenticates and authorizes the request
3. Gateway forwards the request to the appropriate microservice
4. Microservice processes the request and returns a response
5. Gateway performs any post-processing and returns the response to the client

## IMPORTANT NOTES & POSSIBLE TODOs
- Tried to use coroutines on especially i/o operations to boost the performance of gateway. (aiohttp)
- Again, non-blocking db client library is used. (tortoise-orm)
- Tried to use dependency injection on gateway API as a new router, because i am thinking to
  feed this project and make it open source for other people as well.
- Tried to implement declarative way for API gateway rules, for now it works
  based on decorator, but my purpose is to make it more declarative like using
  YAML configuration
- Since it is executed with docker-compose file, it shouldn't be considered as production ready (a.k.a. scalability)
- API gateway approach is considered, also inspired by Zuul, event-driven approach can be easily applied in case needed.
- Authentication and authorization are separated from the services to keep things clean, one service does for all.
- JWT token are generated in gateway service and other services behind the gateway receive a separated
  header called request-user-id to use user specific info.
- thread-safety was not considered especially on fake users service since we
  use file operations, and it might produce race conditions
- Another authorization level can be added into private-network services
  checking if request-user-id header exists
- hashed_password might be shadowed in user's response
- API versioning might be considered
- JWT token TTL can be changed under ./gateway/conf.py[settings]
- Nginx or similar tool can be added in front of all services to leverage more benefits

## Overall Diagram
![ScreenShot](https://raw.github.com/baranbartu/microservices-with-fastapi/master/diagram.png)

## Documentation Page
![ScreenShot](https://raw.github.com/baranbartu/microservices-with-fastapi/master/docs.png)