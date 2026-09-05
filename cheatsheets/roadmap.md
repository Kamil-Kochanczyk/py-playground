This 12-week study plan focuses on software engineering principles, API design, database architecture, and deployment pipeline practices.

Each 3-week module builds toward a milestone project to ensure real-world competency.

---

### Phase 1: Deep Python & Software Engineering (Weeks 1–3)

**Goal:** Transition from basic scripts to writing production-ready, type-safe, and asynchronous code.

* **Week 1: Type Safety & Modern Tooling**
* **Topics:** Modern dependency management using `uv` or `Poetry`; strict static type hints using `typing` (`Optional`, `Union`, `Callable`, `TypeVar`); validation with **Pydantic v2**.
* **Practice:** Configure a project repo from scratch using `uv`, structured with a `pyproject.toml`, formatted with `Ruff`, and checked via `mypy` with zero type errors.


* **Week 2: Asynchronous Programming (`asyncio`)**
* **Topics:** Event loops, coroutines, `async/await`, `asyncio.gather`, handling concurrent network requests, understanding concurrency vs. parallelism (GIL/multiprocessing).
* **Practice:** Write an asynchronous Web Scraper / API aggregator using `httpx` and `asyncio` that fetches data from 10+ endpoints concurrently without blocking.


* **Week 3: Advanced OOP, Generators & Decorators**
* **Topics:** Custom decorators with arguments using `functools.wraps`, context managers (`__enter__`/`__exit__` and `@contextmanager`), generators (`yield`) for memory-efficient data stream handling.
* **Practice:** Create a custom decorator that measures execution time, logs errors to a file, and retries failed API calls up to 3 times before raising an exception.



---

### Phase 2: Production APIs & Databases (Weeks 4–6)

**Goal:** Build fast REST APIs backed by relational databases, ORMs, and caching layers.

* **Week 4: Web Frameworks (FastAPI)**
* **Topics:** FastAPI app structure, routing, Dependency Injection system (`Depends`), status codes, response models, handling background tasks.
* **Practice:** Build a RESTful **Task Management API** featuring request/response validation, custom error handling middleware, and auto-generated Swagger documentation.


* **Week 5: Relational Databases & ORMs (PostgreSQL + SQLAlchemy)**
* **Topics:** SQL queries (JOINs, GROUP BY, Indexing), **SQLAlchemy 2.0** async ORM, schema migrations with **Alembic**, database relationships (one-to-many, many-to-many).
* **Practice:** Connect your FastAPI app to a PostgreSQL database using SQLAlchemy. Create models for `Users` and `Tasks`, write migrations via Alembic, and optimize queries to avoid the N+1 problem.


* **Week 6: Caching & Authentication**
* **Topics:** Password hashing (`passlib`/`bcrypt`), **JWT (JSON Web Tokens)** authentication, **Redis** integration for route caching and rate limiting.
* **Practice:** Implement full JWT User Sign-up/Login flows in your FastAPI application and use Redis to cache user profiles and enforce API rate limits (e.g., max 100 requests/minute).



---

### Phase 3: Testing, Background Tasks & Architecture (Weeks 7–9)

**Goal:** Guarantee code quality with automated test suites and offload heavy work to background workers.

* **Week 7: Automated Testing (`pytest`)**
* **Topics:** Unit tests, integration tests, test fixtures, parametrization, mocking external services (`unittest.mock` / `pytest-mock`), checking coverage (`pytest-cov`).
* **Practice:** Write a comprehensive test suite for your FastAPI application targeting **>85% test coverage**, using an isolated in-memory or Dockerized test database.


* **Week 8: Asynchronous Task Queues (Celery/RQ + Redis)**
* **Topics:** Asynchronous background jobs, message brokers (Redis/RabbitMQ), job retries, scheduled tasks (cron jobs in Celery/RQ).
* **Practice:** Offload long-running tasks from your API (e.g., generating PDF reports or sending confirmation emails) to a **Celery** worker queue.


* **Week 9: Software Architecture & Design Patterns**
* **Topics:** Repository pattern, Service-Repository architecture, Dependency Inversion, SOLID principles, structured JSON logging (`structlog`).
* **Practice:** Refactor your project into a clean 3-tier architecture: **API Layer** (Routes) -> **Service Layer** (Business Logic) -> **Repository Layer** (Database Queries).



---

### Phase 4: Containerization, DevOps & Deployment (Weeks 10–12)

**Goal:** Package, automate, and deploy your entire application stack to the cloud.

* **Week 10: Docker & Containerization**
* **Topics:** `Dockerfile` best practices, multi-stage builds (for minimal image sizes), `.dockerignore`, `docker-compose` for multi-container local environments.
* **Practice:** Containerize your FastAPI backend, PostgreSQL database, Redis server, and Celery worker using a single `docker-compose.yml` file.


* **Week 11: CI/CD Pipelines & Cloud Basics**
* **Topics:** **GitHub Actions** pipelines, running automated tests and linters on Pull Requests, secret management (`.env` files), basic cloud hosting concepts (AWS EC2/App Runner, Render, or Hetzner).
* **Practice:** Set up a GitHub Actions workflow that automatically runs `Ruff`, `mypy`, and `pytest` on every push. Deploy your containerized app live on a platform like Render or AWS.


* **Week 12: Production Monitoring & Capstone Finalization**
* **Topics:** Error tracking via **Sentry**, health check endpoints, database connection pooling tuning, API security basics.
* **Practice:** Integrate Sentry into your live API to catch runtime uncaught exceptions, write a clean `README.md` with setup instructions and architectural diagrams, and pin your capstone project on GitHub.



---

### Suggested Milestone Portfolio Project

By **Week 12**, you should have a single multi-container backend service on GitHub that includes:

1. **FastAPI** backend with asynchronous routes and OpenAPI docs.
2. **PostgreSQL** database managed via **SQLAlchemy 2.0** and **Alembic** migrations.
3. **Redis & Celery** for caching, rate limiting, and background email processing.
4. **pytest** suite with >80% code coverage.
5. **Docker Compose** setup for local orchestration.
6. **GitHub Actions CI/CD** pipeline deploying to a live cloud server.