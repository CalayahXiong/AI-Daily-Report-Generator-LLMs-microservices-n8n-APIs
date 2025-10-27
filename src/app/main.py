from fastapi import FastAPI
from agent import run_agent, fetch_github_updates

from pydantic import BaseModel

app = FastAPI()


class InputData(BaseModel):
    task: str
    custom_prompt: str
    github_repo: str


@app.post("/process")
def process(data: InputData):
    # 如果传了 github_repo，就抓取 GitHub 更新
    if data.github_repo:
        github_summary = fetch_github_updates(data.github_repo)
        task_text = github_summary
    else:
        task_text = data.task

    # 调用 run_agent
    result = run_agent(task=task_text, custom_prompt=data.custom_prompt)

    return {"response": result}
