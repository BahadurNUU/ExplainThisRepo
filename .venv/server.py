from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import shutil
import uuid
import os

from main import clone_git_repo, scan_project, generate_readme_summary, save_readme

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
        readme_content = generate_readme_summary(file_list, repo_path)


        readme_path = os.path.join(repo_path, "README.md")
        save_readme(readme_content, repo_path)


        output_readme_path = os.path.join(temp_folder, "README_to_download.md")
        shutil.copy(readme_path, output_readme_path)


        shutil.rmtree(repo_path)


        return FileResponse(
            path=output_readme_path,
            filename="README.md",
            media_type="text/markdown"
        )

    except Exception as e:
        return {"error": str(e)}
