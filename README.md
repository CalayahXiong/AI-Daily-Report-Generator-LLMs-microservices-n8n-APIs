# AI Daily Report Generator
# AI Automation: Build LLM Apps & AI Agents with n8n + APIs

The AI Daily Report Generator is an end-to-end automation system that creates and delivers daily project summaries using large language models (LLMs) and n8n workflows.
It connects to your data sources (GitHub, Notion, databases, etc.), extracts key updates, summarizes them with GhatGrop, and automatically sends a formatted report via Slack, email, or other channels.

## Features

- Automated Daily Summaries — generate concise project updates with LLMs

- Data Integration — pull context from GitHub commits, Notion pages, CRMs, or APIs

- Workflow Orchestration — coordinate multi-step automation with n8n

- Customizable Reporting — format and deliver results to email, or dashboards

- Extendable Architecture — easily add new data connectors, report styles, or agents

- LLM Flexibility — supports OpenAI, Claude, or Groq models via LangChain

- One-Click Deployment — run locally or in the cloud with Docker Compose

## Presentation
n8n: http://localhost:5678/

HTTP post url: http://api:8000/daily_report

FastAPI: http://localhost:8000/docs#/default/daily_report_daily_report_post

<img width="1117" height="485" alt="image" src="https://github.com/user-attachments/assets/9273d46d-48a7-4d40-a07e-ce5c199db049" />
For the [send_email] node, when trying to send mail via Gmail SMTP in n8n (or any app), use a special App Password: https://myaccount.google.com/apppasswords

<img width="1068" height="389" alt="image" src="https://github.com/user-attachments/assets/97a483f3-e4c7-4414-b3f7-b390b686cc79" />

