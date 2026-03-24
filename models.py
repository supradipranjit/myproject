from sqlalchemy import Column, Integer, String, Text
from database import Base

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String)
    pr_number = Column(Integer)
    diff = Column(Text)