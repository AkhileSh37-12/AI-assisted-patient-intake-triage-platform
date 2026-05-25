# AI-Assisted Patient Intake and Triage Platform

## Overview

AI-Assisted Patient Intake and Triage Platform is a healthcare workflow automation system designed to streamline hospital patient intake, urgency classification, queue management, and doctor consultation workflows using AI-assisted processing and Retrieval-Augmented Generation (RAG) architecture.

The system is built using FastAPI, PostgreSQL, SQLAlchemy ORM, Docker, and modular enterprise backend architecture.

---

## Features

* AI-assisted patient intake workflow
* Voice/Text symptom input support
* Urgency classification
* Department recommendation
* Queue management system
* Doctor consultation workflow
* Activity logging
* AI processing logs
* RAG knowledge base foundation
* Dockerized backend deployment
* Swagger API documentation

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Pydantic
* Docker
* Docker Compose

### AI Architecture

* RAG-ready architecture
* AI orchestration layer
* AI processing logs
* Retrieval logging system
* pgvector support (planned)

---

## Backend Architecture

```plaintext
Route → Service → Database
```

Project follows modular enterprise architecture:

```plaintext
backend/
 └── app/
      ├── ai/
      ├── core/
      ├── db/
      ├── models/
      ├── routes/
      ├── schemas/
      ├── services/
      └── main.py
```

---

## Implemented Modules

* Patients
* Departments
* Roles
* Users
* Doctors
* Patient Intakes
* Queue Entries
* Consultations
* Activity Logs
* AI Processing Logs
* RAG Knowledge Base
* RAG Retrieval Logs

---

## Docker Setup

### Run Containers

```bash
docker compose up --build
```

### Swagger Documentation

```plaintext
http://127.0.0.1:8000/docs
```

---

## Future Enhancements

* Gemini API integration
* pgvector embedding search
* Full RAG retrieval pipeline
* Async AI orchestration
* Real-time queue analytics
* Frontend dashboard
* Speech-to-text integration

---

## Author

Akhilesh Reddy
