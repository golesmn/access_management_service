
# Access Management Service

This repository contains the **Access Management Service**, an independent microservice implemented as a [Fission](https://fission.io/) function. It provides user access and authentication capabilities and is designed following **Domain-Driven Design (DDD)** principles along with the **Repository** and **Service** patterns.

---

## 📁 Project Structure

```
access_management/
├── application/        # Commands and service logic
├── domain/             # Aggregates, value objects, domain events
├── handlers/           # Command and event handlers
├── infrastructure/     # ORM models and other infra details, repositories
├── interfaces/         # Interfaces for external interactions
├── main.py             # Entry point for the function
├── requirements.txt    # Dependencies
shared/                 # Shared abstractions (DB, messaging, etc.)
specs/                  # Fission deployment configs and routes
```

---

## 🧠 Design Patterns Used

### Domain-Driven Design (DDD)

* Domain layer contains aggregates, entities, value objects, and events.
* Business logic is encapsulated in aggregates like `User`.

### Repository Pattern

* Abstracts data access via repository interfaces and implementations like `user_repository.py`.

### Service Pattern

* Encapsulates application-specific logic in `services/user_service.py`.

---

## 🚀 Fission Deployment

The `specs/` directory contains the YAML specifications to deploy this service as a Fission function:

* `function-access-management-producer.yaml`: Registers the function.
* `route-login-route.yaml`: Maps HTTP route to login logic.
* `route-producer-route.yaml`: Maps HTTP route to user creation or messaging.
* `fission-deployment-config.yaml`: Additional deployment configuration.

Deploy all resources using:

```bash
fission spec apply --specdir specs
```

## 📄 Example Event Flow (User Creation)

1. Request hits Fission route → triggers function
2. Handler receives command (e.g. `CreateUser`)
3. Handler delegates to `UserService`
4. Service constructs and persists domain aggregate
5. Domain event `UserCreated` is dispatched (e.g., to Kafka)

---
