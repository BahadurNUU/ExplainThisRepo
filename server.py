from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os
from utils import clear_markdown

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
        readme_content = clear_markdown(readme_content)

        # Clean up
        shutil.rmtree(repo_path)

        return JSONResponse(content={"markdown": readme_content})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


app.mount("/", StaticFiles(directory="client/dist", html=True), name="static")

# Optional: fallback to index.html for SPA routing
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    file_path = os.path.join("client/dist", "index.html")
    return FileResponse(file_path)