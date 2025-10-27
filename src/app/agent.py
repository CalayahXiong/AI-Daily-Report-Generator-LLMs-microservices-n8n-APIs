import os
from datetime import datetime, timedelta

import requests
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


def call_custom_api(input_text: str) -> str:
    """
    调用本地 FastAPI microservice
    """
    try:
        r = requests.post(
            "http://api:8000/process",
            json={"task": input_text}  # 注意这里使用 task，和 FastAPI InputData 对应
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
    调用 ChatGroq 生成摘要或处理任务
    如果 custom_prompt 有值，会作为系统提示覆盖默认行为
    """
    messages = []

    if custom_prompt:
        messages.append(SystemMessage(content=custom_prompt))

    messages.append(HumanMessage(content=task))

    # 调用 ChatGroq
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error calling LLM: {e}"


def fetch_github_updates(repo: str) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}

    since = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    pr_url = f"https://api.github.com/repos/{repo}/pulls?state=all&sort=updated&direction=desc"

    response = requests.get(pr_url, headers=headers)
    if response.status_code != 200:
        return f"Error fetching PRs: {response.status_code} {response.text}"

    try:
        prs = response.json()
    except Exception as e:
        return f"Error parsing JSON: {e}"

    recent_prs = [pr for pr in prs if pr.get("updated_at") >= since]

    summary = f"GitHub Updates for {repo} in last 24h:\n"
    for pr in recent_prs:
        summary += f"- PR #{pr['number']}: {pr['title']} by {pr['user']['login']}\n"

    return summary
