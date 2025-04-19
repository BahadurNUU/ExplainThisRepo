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

def convert_py2_to_py3(repo_path):
    print("Converting Python 2 code to Python 3 using 2to3...")
    try:
        subprocess.run(["2to3", "-w", repo_path], check=True)
        print("Conversion complete.")
    except subprocess.CalledProcessError as e:
        print(f"2to3 failed: {e}")

def analyze_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"SyntaxError in {file_path}: {e}")
        return {"functions": [], "classes": [], "content": content}

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {"functions": functions, "classes": classes, "content": content}

def analyze_js_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    functions = re.findall(r"function (\w+)", content)
    return {"functions": functions, "classes": [], "content": content}

def scan_project(repo_path):
    print(f"Scanning the project at {repo_path}...")
    file_summary = []

    valid_extensions = (
        ".py", ".js", ".ts", ".java", ".md", "Dockerfile",
        ".jsx", ".tsx", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx",
        ".class", ".jar", ".ipynb", ".sh", ".bash", ".zsh", ".bat", ".cmd", ".ps1",
        ".rb", ".go", ".swift", ".kt", ".kts", ".sql", ".pl", ".pm", ".cs", ".csproj",
        ".vb", ".fs", ".fsx", ".dart", ".r", ".ex", ".exs", ".clj", ".cljs", ".edn",
        ".lisp", ".lsp", ".el", ".ml", ".mli", ".fsproj", ".vcxproj", ".pro", ".xml",
        ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".env", ".gitattributes",
        ".gitignore", ".gitmodules", ".lock", ".txt", ".rst", ".log", ".scss", ".sass",
        ".less", ".css", ".html", ".htm", ".xsl", ".xsd", ".vue", ".svelte", ".astro",
        ".res", ".resx", ".njk", ".ejs", ".hbs", ".mustache", ".twig", ".erl", ".hrl",
        ".dart_tool", ".gradle", ".build.gradle", ".pom", ".make", ".mk", ".Makefile",
        ".CMakeLists.txt", ".dockerignore", ".editorconfig", ".npmrc", ".yarnrc", ".babelrc",
        ".eslintrc", ".stylelintrc", ".prettierrc", ".postcssrc", ".nodemon.json", ".terraform",
        ".tf", ".tfvars", ".lock.json", ".config.js", ".config.ts", ".vue.config.js",
        "jest.config.js", "webpack.config.js", "rollup.config.js", "vite.config.js", "next.config.js"
    )

    for root, _, files in os.walk(repo_path):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(valid_extensions):
                if file.endswith(".py"):
                    result = analyze_python_file(full_path)
                elif file.endswith(".js") or file.endswith(".ts"):
                    result = analyze_js_file(full_path)
                else:
                    result = {"functions": [], "classes": [], "content": ""}

                file_summary.append({
                    "file_path": full_path,
                    "functions": result["functions"],
                    "classes": result["classes"],
                    "content": result["content"]
                })

    return file_summary

def generate_readme_summary(file_list, repo_path):
    prompt = f"""You are an expert developer. Based on the following file structure and content analysis, generate a detailed README.md for this project.

Project files and their content:
{chr(10).join([f"File: {file['file_path']} | Functions: {', '.join(file['functions'])} | Classes: {', '.join(file['classes'])}" for file in file_list])}

The README should include:
- Project title
- Description of what each file does
- Installation instructions
- Usage examples
- Technologies used
- License section (guess if possible)
- Contribution guidelines

Be creative and helpful. Do not just write an overview. Provide details of the functionality from the code itself."""

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

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

        convert_py2_to_py3(repo_path)  # 👈 Auto-convert Python 2 code

        file_list = scan_project(repo_path)
        print(f"Scanned {len(file_list)} files")

        readme_content = generate_readme_summary(file_list, repo_path)
        print("Generated README.md content")

        save_readme(readme_content, repo_path)
        print("README.md saved successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
