from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import shutil
import uuid
import os

from main import clone_git_repo, scan_project, generate_docs

app = FastAPI()

class RepoRequest(BaseModel):
    repo_url: str

@app.post("/api/process-repo")
async def process_repo(data: RepoRequest):
    try:
        temp_folder = f"cloned_repo/{uuid.uuid4().hex}"
        os.makedirs(temp_folder, exist_ok=True)

        repo_path = clone_git_repo(data.repo_url, clone_dir=temp_folder)
        file_list = scan_project(repo_path)
        readme_content = generate_docs(file_list)

        # Clean up
        shutil.rmtree(repo_path)

        return JSONResponse(content={"markdown": readme_content})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )