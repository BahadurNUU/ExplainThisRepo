import os
import git
import google.generativeai as genai
from dotenv import load_dotenv
import ast
import re
import subprocess

load_dotenv()

API_KEY = os.environ['API_KEY']
genai.configure(api_key=API_KEY)

def clone_git_repo(github_url, clone_dir="cloned_repo"):
    repo_name = github_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(clone_dir, repo_name)

    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    print(f"Cloning git repository {github_url} to {repo_path}...")
    git.Repo.clone_from(github_url, repo_path)

    return repo_path


def scan_project(repo_path):
    """
    Traverse the directory and read source code files.

    :param repo_path: Root path of the cloned GitHub repo.
    :param valid_extensions: A set of extensions to include, or None to read all text files.
    :return: A list of tuples (relative_path, file_content).
    """
    collected_files = []


    valid_extensions = ['.py', '.js', '.ts', '.java', '.html', '.css', '.jsx', '.tsx', '.md', '.cpp']

    for root, _, files in os.walk(repo_path):
        for filename in files:
            file_ext = os.path.splitext(filename)[1]

            if file_ext in valid_extensions:
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        relative_path = os.path.relpath(file_path, repo_path)
                        collected_files.append((relative_path, content))
                except Exception as e:
                    print(f"Skipped {filename}: {e}")
    
    return collected_files

def generate_readme(file_path, file_content):
    prompt = f"""
        You are a professional readme documentation generator. 
        Your task is to write a detailed explanation of the provided code file.
        Make sure the documentation is clear and structured.
        The documentation has to be written in Markdown format.
        Important: Do not write any comments. Generate the markdown content without surrounding it with triple backticks.
        You need to return only the raw markdown text itself.
        File name: {file_path} \n
        File content:  {file_content}
    """

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

def generate_docs(collected_files):
    readme_docs = []

    for path, content in collected_files:
        readme = generate_readme(path, content)
        readme_docs.append(readme)
    
    return '\n'.join(readme_docs)
    


def save_readme(content, repo_path):
    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(content)
    print(f"README.md saved to {readme_path}")

def main():
    github_url = input("Enter GitHub repository URL: ").strip()
    print("Starting repository processing...")
    try:
        repo_path = clone_git_repo(github_url)
        print(f"Cloned repository to {repo_path}")

        file_list = scan_project(repo_path)
        print(f"Scanned {len(file_list)} files")

        readme_content = generate_readme_summary(file_list)
        print("Generated README.md content")

        save_readme(readme_content, repo_path)
        print("README.md saved successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
