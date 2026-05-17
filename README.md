# DistTask

A lightweight distributed task queue framework inspired by Celery, built for learning distributed systems, asynchronous processing, retries, scheduling, and worker orchestration.

DistTask focuses on clean architecture and production-inspired backend concepts instead of trying to fully replicate Celery.

---

# Features

## Current Features

### Core Task Queue
- Distributed task execution
- Redis-backed message broker
- Async task submission
- Multiple worker support
- Task acknowledgment handling

### Worker System
- Concurrent task processing
- Worker heartbeat tracking
- Graceful shutdown
- Task prefetching
- Visibility timeout support

### Task Management
- Task decorators
- Dynamic task registry
- Retry support
- Exponential backoff retries
- Dead-letter queue support

### Scheduling
- ETA-based task scheduling
- Delayed task execution
- Scheduler service

### Result Backend
- Task state tracking
- Result persistence
- Failure tracking
- Execution metadata

### Monitoring
- Real-time worker monitoring
- Queue statistics
- Failed task tracking
- Retry statistics
- Execution latency metrics

### API
- Task submission APIs
- Task status APIs
- Queue inspection APIs

---

# System Architecture

```text
                +-------------------+
                |   Client/API      |
                +-------------------+
                          |
                          v
                +-------------------+
                |   Task Producer   |
                +-------------------+
                          |
                          v
                +-------------------+
                |   Redis Broker    |
                +-------------------+
                   |            |
                   |            |
                   v            v
           +-------------+ +-------------+
           | Worker-1    | | Worker-2    |
           +-------------+ +-------------+
                   |
                   v
          +--------------------+
          | Result Backend     |
          +--------------------+
                   |
                   v
          +--------------------+
          | Monitoring API     |
          +--------------------+
```

---

# Tech Stack

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| Broker | Redis |
| Database | PostgreSQL |
| Worker Runtime | asyncio + multiprocessing |
| Monitoring | Prometheus |
| Dashboard | Grafana |
| Containerization | Docker |
| Orchestration | Docker Compose |

---

# Project Structure

```text
DistTask/
│
├── api/
│   ├── routes/
│   ├── schemas/
│   └── dependencies/
│
├── broker/
│   ├── redis_broker.py
│   ├── queue.py
│   └── visibility_timeout.py
│
├── worker/
│   ├── worker.py
│   ├── executor.py
│   ├── heartbeat.py
│   └── concurrency.py
│
├── scheduler/
│   ├── scheduler.py
│   └── delayed_queue.py
│
├── retries/
│   ├── retry_manager.py
│   └── backoff.py
│
├── result_backend/
│   ├── redis_backend.py
│   └── postgres_backend.py
│
├── monitoring/
│   ├── metrics.py
│   ├── logging.py
│   └── tracing.py
│
├── registry/
│   ├── task_registry.py
│   └── decorators.py
│
├── serialization/
│   ├── serializer.py
│   └── models.py
│
├── cli/
│   ├── worker_cli.py
│   └── scheduler_cli.py
│
├── tests/
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# Getting Started

## Prerequisites

- Python 3.11+
- Redis
- Docker (optional)

---

# Installation

```bash
git clone https://github.com/yourusername/DistTask.git

cd DistTask

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

---

# Run Redis

```bash
docker run -p 6379:6379 redis
```

---

# Start API Server

```bash
uvicorn api.main:app --reload
```

---

# Start Worker

```bash
python -m cli.worker_cli
```

---

# Start Scheduler

```bash
python -m cli.scheduler_cli
```

---

# Example Usage

## Define Task

```python
from DistTask import app


@app.task(
    retries=3,
    retry_backoff=True,
    timeout=30
)
def process_image(image_id):
    print(f"Processing image: {image_id}")
```

---

## Submit Task

```python
process_image.delay(123)
```

---

## Schedule Task

```python
process_image.apply_async(
    args=[123],
    countdown=60
)
```

---

# Task Lifecycle

```text
PENDING
   ↓
QUEUED
   ↓
STARTED
   ↓
SUCCESS / FAILURE
   ↓
RETRY (optional)
```

---

# Reliability Features

## Visibility Timeout

If a worker crashes before acknowledging a task:

- task becomes visible again
- another worker can process it
- ensures at-least-once delivery

---

## Retry System

Supports:
- configurable retry count
- exponential backoff
- delayed retries
- dead-letter queue

Example:

```python
@app.task(retries=5)
def send_email():
    ...
```

---

# Monitoring

Metrics exposed:
- queued tasks
- active workers
- task throughput
- retry count
- failed tasks
- task latency

---

# API Endpoints

## Submit Task

```http
POST /tasks
```

---

## Get Task Status

```http
GET /tasks/{task_id}
```

---

## Queue Statistics

```http
GET /queues/stats
```

---

# Development Goals

This project is focused on learning:
- distributed systems fundamentals
- asynchronous processing
- fault tolerance
- worker orchestration
- retries and scheduling
- observability
- backend system design

---

# TODO Roadmap

# Phase 1 — MVP

## Core Queue
- [ ] Redis queue implementation
- [ ] Task producer
- [ ] Worker polling
- [ ] Task execution
- [ ] Task serialization
- [ ] Result backend
- [ ] Task states

## Worker Runtime
- [ ] Multiprocessing workers
- [ ] Async execution engine
- [ ] Graceful shutdown
- [ ] Worker concurrency configuration

## Retry System
- [ ] Retry counter
- [ ] Exponential backoff
- [ ] Delayed retries

---

# Phase 2 — Reliability

## Queue Reliability
- [ ] Visibility timeout
- [ ] Acknowledgement system
- [ ] Worker crash recovery
- [ ] Dead-letter queue

## Scheduling
- [ ] ETA tasks
- [ ] Countdown tasks
- [ ] Scheduler service

## Monitoring
- [ ] Metrics endpoint
- [ ] Worker health API
- [ ] Queue stats API
- [ ] Structured logging

---

# Phase 3 — Production Features

## Advanced Worker Features
- [ ] Dynamic worker scaling
- [ ] Worker heartbeat
- [ ] Queue prefetch limits
- [ ] Worker auto-recovery

## Rate Limiting
- [ ] Token bucket limiter
- [ ] Per-task rate limits
- [ ] Global rate limiting

## Priority Queues
- [ ] High priority queues
- [ ] Medium priority queues
- [ ] Low priority queues

---

# Phase 4 — Observability

## Monitoring Dashboard
- [ ] Live queue metrics
- [ ] Task execution timeline
- [ ] Retry visualization
- [ ] Worker monitoring dashboard

## Tracing
- [ ] OpenTelemetry integration
- [ ] Distributed tracing
- [ ] Request correlation IDs

---

# Phase 5 — Future Improvements

## Broker Support
- [ ] RabbitMQ broker
- [ ] Kafka broker

## Deployment
- [ ] Kubernetes deployment
- [ ] Helm charts
- [ ] ECS deployment

## Security
- [ ] Task authentication
- [ ] API authentication
- [ ] Queue authorization

---

# Non-Goals

The following are intentionally out of scope:

- Exactly-once delivery guarantees
- Distributed consensus
- Multi-region replication
- Full Celery compatibility
- Workflow DAG engine
- Distributed transactions

---

# Key Engineering Concepts Demonstrated

- Distributed systems
- Asynchronous processing
- Queue-based architecture
- Fault tolerance
- Worker orchestration
- Retry semantics
- Scheduling systems
- Observability
- Idempotency
- At-least-once delivery

---

# Example Resume Description

Built a distributed Python task queue framework inspired by Celery supporting asynchronous task scheduling, retries with exponential backoff, Redis-backed queues, worker heartbeats, and real-time monitoring APIs.

---

# License

MIT License
