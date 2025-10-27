import os
import sqlite3
from datetime import datetime, timedelta

import requests
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


def call_custom_api(input_text: str) -> str:
    """
    call FastAPI microservice loally
    """
    try:
        r = requests.post(
            "http://api:8000/process",
            json={"task": input_text}
        )
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        return f"Error calling custom API: {e}"


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key= os.environ.get("GROQ_API_KEY")
)


def run_agent(task: str, custom_prompt: str) -> str:
    """
    call ChatGroq handle the task
    custom_prompt: a guiding sentence like telling ai how to behave for more accurate responses
    """
    messages = []

    if custom_prompt:
        messages.append(SystemMessage(content=custom_prompt))

    messages.append(HumanMessage(content=task))

    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error calling LLM: {e}"


def fetch_github_updates(repo: str) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"

    # --- get Pull Requests ---
    pr_url = f"https://api.github.com/repos/{repo}/pulls?state=all&sort=updated&direction=desc"
    prs_response = requests.get(pr_url, headers=headers)
    prs = prs_response.json() if prs_response.status_code == 200 else []

    # --- get Commits ---
    commits_url = f"https://api.github.com/repos/{repo}/commits?since={since}"
    commits_response = requests.get(commits_url, headers=headers)
    commits = commits_response.json() if commits_response.status_code == 200 else []

    summary_lines = [f"### GitHub Updates for {repo} in last 24h"]

    recent_prs = [pr for pr in prs if pr.get("updated_at", "") >= since]
    if recent_prs:
        summary_lines.append("\n**Pull Requests:**")
        for pr in recent_prs:
            summary_lines.append(f"- #{pr['number']}: {pr['title']} by {pr['user']['login']}")
    else:
        summary_lines.append("\n_No PR updates in the last 24h._")

    if commits:
        summary_lines.append("\n**Commits:**")
        for commit in commits:
            msg = commit["commit"]["message"].split("\n")[0]
            author = commit["commit"]["author"]["name"]
            date = commit["commit"]["author"]["date"]
            summary_lines.append(f"- {msg} ({author}, {date[:10]})")
    else:
        summary_lines.append("\n_No commits in the last 24h._")

    return "\n".join(summary_lines)


def fetch_db_updates(db_path: str) -> str:
    conn = sqlite3.connect(db_path)  # SQLite
    cursor = conn.cursor()

    since = (datetime.utcnow() - timedelta(days=1).isformat())

    cursor.execute("""
        SELECT id, name, updated_at
        FROM records
        WHERE updated_at >= ?
        ORDER BY updated_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    summary_lines = ["### Database updates in last 24 hours"]

    if rows:
        for row in rows:
            summary_lines.append(f"- {row[1]} (updated {row[2]}")
    else:
        summary_lines.append("_No database updates in last 24 hours._")

    return "\n".join(summary_lines)


def fetch_notion_updates(database_id: str) -> str:
    notion_token = os.environ.get("NOTION_TOKEN")
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=headers)

    summary_lines = ["### Notion Updates (last 24h)"]

    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            for page in results:
                title = (
                    page["properties"]["Name"]["title"][0]["plain_text"]
                    if page["properties"]["Name"]["title"]
                    else "Untitled"
                )
                summary_lines.append(f"- {title}")
        else:
            summary_lines.append("_No recent updates._")
    else:
        summary_lines.append(f"Error fetching Notion data: {response.status_code}")

    return "\n".join(summary_lines)

