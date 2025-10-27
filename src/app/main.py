import os

from fastapi import FastAPI
from agent import run_agent, fetch_github_updates, fetch_db_updates, fetch_notion_updates
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel

app = FastAPI()


class InputData(BaseModel):
    task:  str = "Daily project summary"
    custom_prompt: str = "Summarize and highlight key updates from all resources."
    github_repo: str
    db: str
    notion: str


@app.post("/daily report")
def daily_report(data: InputData):

    github_summary = fetch_github_updates(data.github_repo) if data.github_repo else ""
    db_summary = fetch_db_updates(data.db) if data.db else ""
    notion_summary = fetch_notion_updates(data.notion) if data.notion else ""

    combined_report = "\n\n".join([github_summary, db_summary, notion_summary])

    report_summary = run_agent(task=combined_report, custom_prompt=data.custom_prompt)

    send_daily_report_by_email(report_summary, recipient=[
        "mina@gmail.com",
        "jennie@gmail.com",
        "jeonghan@gmail.com"
    ])

    return {"response": report_summary}


def generate_daily_report(data: InputData):
    report_parts = [
        fetch_github_updates(data.github_repo),  # "your_org/your_repo"
        fetch_db_updates(data.db),  # "path/to/db.sqlite"
        fetch_notion_updates(data.notion)  # "your_notion_database_id"
    ]
    return "\n\n".join(report_parts)


def send_daily_report_by_email(report: str, recipients: list[str]):
    msg = MIMEText(report, "plain")
    msg["Subject"] = "Daily Project Report"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        smtp.send_message(msg)
        smtp.sendmail(msg["From"], recipients, msg.as_string())

