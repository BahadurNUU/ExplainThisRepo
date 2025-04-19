from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RepoRequest(BaseModel):
    repo_url:str

@app.post("/api/process-repo")
async def process_repo(data: RepoRequest):
    repo_url = data.repo_url

    return {"message": f"Repo received: {repo_url}"}
