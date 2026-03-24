from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
import requests

from database import SessionLocal
import models

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    print("\nWebhook received!")

    if payload.get("action") == "opened":
        pr = payload["pull_request"]

        repo = payload["repository"]["full_name"]
        pr_number = pr["number"]
        diff_url = pr["diff_url"]

        print("PR Number:", pr_number)

        # Fetch diff
        diff = requests.get(diff_url).text

        # 🔥 STORE IN DATABASE
        new_pr = models.PullRequest(
            repo_name=repo,
            pr_number=pr_number,
            diff=diff
        )

        db.add(new_pr)
        db.commit()

        print("Stored in database!")

    return {"status": "ok"}