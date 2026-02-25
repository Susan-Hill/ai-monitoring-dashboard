# AI Monitoring Dashboard

## Overview
This project implements an AI Monitoring and Observability Dashboard
for a containerized LLM service using:

- FastAPI (AI service layer)
- Ollama (local LLM container)
- Prometheus (metrics backend)
- Grafana (visualization)

## Goals
- Track AI latency
- Track request volume
- Monitor error rates
- Track token usage
- Estimate cost
- Implement reliability alerts

## Architecture (Planned)

Client -> FastAPI Service -> Ollama (LLM) -> Prometheus (Metrics Collection) -> Grafana (Visualization)

## Status
v1 — Initial project structure