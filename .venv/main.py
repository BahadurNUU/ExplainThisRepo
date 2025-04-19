import os
import git
import os
import google.generativeai as genai
from dotenv import load_dotenv

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
            if file.endswith(valid_extensions):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                file_summary.append(rel_path)

    return file_summary


def generate_readme_summary(file_list, repo_path):
    prompt = f"""You are an expert developer. Based on the following file structure, generate a detailed README.md for this project.

Project files:
{chr(10).join(file_list)}

The README should include:
- Project title
- Description
- Installation instructions
- Usage examples
- Technologies used
- License section (guess if possible)
- Contribution guidelines

Be creative and helpful. Do not just write an overview,  You should cover project's every important detail."""

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text


def save_readme(content, repo_path):
    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(content)
    print(f"README.md saved to {readme_path}")


