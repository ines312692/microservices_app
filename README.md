# FastAPI Microservices Application

A modern, scalable microservices architecture built with FastAPI, Docker, Kubernetes, and Jenkins CI/CD pipelines.

## Project Overview

This project demonstrates a microservices architecture using FastAPI for building high-performance APIs. The application consists of three main services:

- **Gateway Service**: API gateway that routes requests to appropriate microservices and handles authentication/authorization
- **Users Service**: Manages user accounts, authentication, and user data
- **Orders Service**: Manages order creation and retrieval

The project is designed to showcase best practices for building, deploying, and scaling microservices using modern cloud-native technologies.

## Architecture

```
┌─────────────┐      ┌─────────────┐
│             │      │             │
│   Clients   │─────▶│   Gateway   │
│             │      │   Service   │
└─────────────┘      └──────┬──────┘
                            │
                            ▼
          ┌─────────────────┴─────────────────┐
          │                                   │
          ▼                                   ▼
┌─────────────────┐               ┌─────────────────┐
│                 │               │                 │
│  Users Service  │               │ Orders Service  │
│                 │               │                 │
└─────────────────┘               └─────────────────┘
```

### Key Technologies

- **FastAPI**: High-performance Python web framework for building APIs
- **Docker**: Containerization for consistent development and deployment
- **Kubernetes**: Container orchestration for scaling and managing services
- **Helm**: Package manager for Kubernetes applications
- **Jenkins**: CI/CD pipelines for automated building and deployment

## Services Description

### Gateway Service

The Gateway Service acts as an API gateway that:
- Routes requests to appropriate microservices
- Handles authentication and authorization
- Provides a unified API interface to clients
- Implements security and access control

### Users Service

The Users Service manages:
- User registration and authentication
- User profile data
- Password hashing and verification
- User authorization levels

### Orders Service

The Orders Service handles:
- Order creation
- Order retrieval
- Order data persistence using SQLite and Tortoise ORM

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Kubernetes cluster (for production deployment)
- Helm (for Kubernetes deployment)
- Jenkins (for CI/CD)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd microservices_app
   ```

2. Create .env files for each service:
   ```bash
   # Example for gateway_service/.env
   USERS_SERVICE_URL=http://users:8000
   ORDERS_SERVICE_URL=http://orders:8000
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the API gateway at http://localhost:8001

## Deployment Instructions

### Kubernetes Deployment

1. Create the namespace:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```

2. Deploy the services using Helm:
   ```bash
   helm upgrade --install users-deploy ./helm/users -f ./helm/users/values.yaml --namespace fastapi-microservices
   helm upgrade --install orders-deploy ./helm/orders -f ./helm/orders/values.yaml --namespace fastapi-microservices
   helm upgrade --install gateway-deploy ./helm/gateway -f ./helm/gateway/values.yaml --namespace fastapi-microservices
   ```

### CI/CD Pipeline

The project includes Jenkins pipelines for automated building and deployment:

1. Build pipelines: Build Docker images and push to registry
2. Deploy pipelines: Deploy services to Kubernetes using Helm

## API Usage Examples

### Authentication

```bash
# Login
curl -X POST http://localhost:8001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'
```

### User Management

```bash
# Create user (requires admin token)
curl -X POST http://localhost:8001/api/users_service \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <admin_token>" \
  -d '{"username": "newuser", "email": "user@example.com", "password": "password", "is_admin": false}'

# Get users (requires admin token)
curl -X GET http://localhost:8001/api/users_service \
  -H "Authorization: Bearer <admin_token>"
```

### Order Management

```bash
# Create order (requires user token)
curl -X POST http://localhost:8001/api/orders_service \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <user_token>" \
  -d '{"product_name": "Product", "quantity": 1, "price": 10.0}'

# Get orders (requires user token)
curl -X GET http://localhost:8001/api/orders_service \
  -H "Authorization: Bearer <user_token>"
```

## Project Structure

```
microservices_app/
│
├── README.md
├── docker-compose.yml
├── helm/                  # Helm charts for Kubernetes deployment
│   ├── gateway/
│   ├── users/
│   ├── orders/
│   └── microservices-app/
├── Jenkins/               # Jenkins CI/CD pipeline configurations
│   ├── build/
│   ├── deploy/
│   └── jenkins-master/
├── k8s/                   # Kubernetes configurations
│   ├── namespace.yaml
│   └── networkpolicy.yaml
├── gateway_service/       # API Gateway service
│   ├── Dockerfile
│   ├── main.py
│   ├── auth.py
│   ├── conf.py
│   ├── core.py
│   ├── exceptions.py
│   ├── network.py
│   ├── post_processing.py
│   ├── requirements.txt
│   └── datastructures/
├── orders_service/        # Orders management service
│   ├── Dockerfile
│   ├── main.py
│   ├── init_db.py
│   ├── models.py
│   └── requirements.txt
└── users_service/         # User management service
    ├── Dockerfile
    ├── main.py
    ├── auth.py
    ├── datastructures.py
    ├── requirements.txt
    ├── fake/
    └── tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Last Updated

2025-08-07