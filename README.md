# Kubernetes Security Audit Agent - Langgraph

## Overview

This is a Kubernetes security audit agent that uses Langgraph to audit the security of a Kubernetes cluster.

## Requirements

- Python 3.10+
- Kubernetes cluster
- Langchain
- Langgraph
- Kubernetes Python SDK
- OpenAI + API key

> you need to add the openai api key to the `.env` file in the root of the project

## Setup

```bash
uv sync
```

## Run

```bash
uv run graph_k8s.py
```